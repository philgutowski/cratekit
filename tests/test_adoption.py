"""U23: library adoption, from the census to the approval to the revert.

WHAT THIS UNIT IS. A person already has a rekordbox library. Adoption reads it,
proposes where each track belongs in the taxonomy they declared, shows them the
whole proposal, and writes only what they approve, a piece at a time, resuming
where it stopped. Nothing about that is hard until you ask what happens to the
tracks the proposal has nothing to say about, and that is where the failures are.

THE SIX SCENARIOS THE BRIEF NAMES, and where each is proved:

1. unreadable and online-only files appear as named categories in the plan
   -> ``test_every_unreadable_shape_appears_as_its_own_named_category``
2. tracks with blank or generic genre have an explicit disposition and never fall
   out of the plan -> ``test_a_blank_or_generic_genre_gets_a_disposition``
   and ``test_the_plan_carries_every_scanned_row_whatever_happened_to_it``
3. a plan approved and applied 30 percent through resumes from item 31
   -> ``test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one``
4. no blanket affirmative flag applies a plan
   -> ``test_no_blanket_affirmative_applies_a_plan`` and the source guard
   ``test_no_module_in_the_adoption_package_reads_the_environment``
5. a tag write is reverted exactly by the revert ledger
   -> ``test_a_tag_write_is_reverted_exactly`` and its absent-field sibling
6. a declared taxonomy folder that already exists with different contents is
   surfaced rather than merged -> ``test_a_declared_folder_that_already_exists_is_surfaced``

WHAT IS SUPPLEMENTED, because the six leave the expensive shapes uncovered. The
identity of a collision under a rename, which is the defect U19 shipped one layer
along. The order of the three writes per entry and what a crash between any two
of them costs. The two readers, against every document that is good JSON and is
not this document. And the lock, proved by real processes rather than by reading
the code, because that is the only thing that can see what reached the disk.

D1 APPLIES TO EVERY NAME HERE. Nothing below names a real volume, a real person,
or a real track.
"""

from __future__ import annotations

import ast
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
import unicodedata
from dataclasses import replace
from pathlib import Path

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import approval as adopt_approval
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import revert as adopt_revert
from cratekit.adopt import scan as adopt_scan
from cratekit.core import cause, config, locations, review, tags, taxonomy
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from tests.test_config import valid_data
from tests.test_tags import _synth

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
ADOPT_ROOT = SRC_ROOT / "cratekit" / "adopt"

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
HANDLER = "adopt.scan"

#: One name in each composition form, because the pair is the whole reason the
#: identity primitives exist and a ledger keyed on the raw string holds two
#: records for one file.
COMPOSED = "Café One.flac"
DECOMPOSED = unicodedata.normalize("NFD", COMPOSED)


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library, monkeypatch):
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    return resolved


@pytest.fixture
def declared():
    return taxonomy.default_taxonomy()


@pytest.fixture
def store(cfg):
    with review.open_store(cfg) as opened:
        yield opened


def _bucket_and_genre(declared_taxonomy) -> tuple[str, str]:
    """A bucket the shipped template really declares, and a genre that reaches it.

    DERIVED rather than named. A test that spells a bucket identifier is a test
    that has to be edited when the shipped template moves, and R19 says the
    template is the user's to replace.
    """
    for bucket in declared_taxonomy.buckets:
        if bucket.id == declared_taxonomy.fallback.bucket:
            continue
        resolution = adopt_scan.routing.resolve_bucket(declared_taxonomy, bucket.display)
        if resolution.bucket_id == bucket.id and resolution.match is not (
            adopt_scan.routing.Match.FALLBACK
        ):
            return bucket.id, bucket.display
    raise AssertionError("the shipped template declares no routable bucket")


def _row(cfg_value, name: str, genre: str, content_id: str) -> adopt_scan.CollectionRow:
    return adopt_scan.CollectionRow(
        content_id=content_id,
        recorded=f"{cfg_value.library.root}/Music/{name}",
        genre=genre,
        deleted=False,
    )


def _synth_in(directory: Path, suffix: str) -> Path:
    """``_synth`` into a directory that may not exist yet. It does not mkdir."""
    directory.mkdir(parents=True, exist_ok=True)
    return _synth(directory, suffix)


def _readable(_path: Path) -> adopt_scan.Readability:
    """A probe that says every file is fine, for tests about something else."""
    return adopt_scan.Readability.READABLE


def _plan_of(cfg_value, declared_taxonomy, rows, *, existing=()) -> adopt_plan.AdoptionPlan:
    scanned = list(
        adopt_scan.scan_rows(
            rows, declared_taxonomy, root=cfg_value.library.root, probe=_readable
        )
    )
    return adopt_plan.build_adoption_plan(
        scanned, declared_taxonomy, tree=TREE_ID, existing=existing
    )


def _in_separate_processes(script: str, *, workers: int, arguments) -> None:
    """Run one short script in several REAL interpreters at once, and check each.

    A thread shares this interpreter's memory and its locks, so it can only ever
    prove that a value was kept in a variable. Only a separate process can show
    what actually reached the disk, which is the whole question a lock has to
    answer. Copied in shape from ``tests/test_review_queue.py``, which proved the
    same property for the decision stores after eight real processes lost 122 of
    200 records without one.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    running = [
        subprocess.Popen(
            [sys.executable, "-c", script, *(str(value) for value in arguments(worker))],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for worker in range(workers)
    ]
    for process in running:
        out, err = process.communicate()
        assert process.returncode == 0, err or out


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 1: every unreadable shape is a NAMED category, never an omission
# ═══════════════════════════════════════════════════════════════════════════


def test_every_unreadable_shape_appears_as_its_own_named_category(cfg, declared, tmp_path):
    """AE12, and the reason it is an acceptance criterion rather than a nicety.

    A library holding cloud-backed files produced a plan quietly covering fewer
    tracks than the library has, and nothing in the output said so. Each shape
    gets its own name here because their remedies differ: a missing file wants a
    drive, an online-only one wants a download, an unmapped prefix wants
    configuration, and a pseudo-location wants nothing at all.
    """
    music = Path(cfg.library.root) / "Music"
    present = music / "Present.flac"
    present.write_bytes(b"audio")
    evicted = music / "Evicted.flac"
    (music / ".Evicted.flac.icloud").write_bytes(b"")
    unreadable = music / "Locked.flac"
    unreadable.write_bytes(b"audio")

    def probe(path: Path) -> adopt_scan.Readability:
        if path.name == "Locked.flac":
            return adopt_scan.Readability.UNREADABLE
        return adopt_scan.probe_readability(path)

    rows = [
        adopt_scan.CollectionRow(str(present), str(present), "House", False),
        adopt_scan.CollectionRow(str(evicted), str(evicted), "House", False),
        adopt_scan.CollectionRow(str(unreadable), str(unreadable), "House", False),
        adopt_scan.CollectionRow("gone", str(music / "Gone.flac"), "House", False),
        adopt_scan.CollectionRow("elsewhere", "/SomewhereElse/x.flac", "House", False),
        adopt_scan.CollectionRow("stream", "provider:track:9", "House", False),
    ]
    scanned = list(
        adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=probe)
    )
    found = {track.content_id: track.readability for track in scanned}

    assert found[str(present)] is adopt_scan.Readability.READABLE
    assert found[str(evicted)] is adopt_scan.Readability.ONLINE_ONLY
    assert found[str(unreadable)] is adopt_scan.Readability.UNREADABLE
    assert found["gone"] is adopt_scan.Readability.MISSING
    assert found["elsewhere"] is adopt_scan.Readability.UNMAPPED
    assert found["stream"] is adopt_scan.Readability.NOT_A_PATH

    counts = adopt_scan.categories(scanned)
    assert set(counts) == {str(member) for member in adopt_scan.Readability}, (
        "the summary lists only the categories it happened to see, so 'no "
        "online-only files here' and 'this build does not look for them' are "
        "the same output"
    )
    assert counts[str(adopt_scan.Readability.ONLINE_ONLY)] == 1


def test_an_online_only_file_is_never_opened_by_the_probe(cfg, monkeypatch):
    """Opening a dataless file triggers a download, per file, across a library.

    So the platform's own dataless flag is asked instead. A probe that read the
    first byte to find out whether it could would fetch the whole library from
    the provider, which is the opposite of a scan.
    """
    music = Path(cfg.library.root) / "Music"
    dataless = music / "Dataless.flac"
    dataless.write_bytes(b"audio")
    real_stat = Path.stat

    class _Stat:
        # THE LITERAL, not the constant the probe compares against. Setting it
        # from ``adopt_scan.DATALESS_FLAG`` made this assertion "the guard fires
        # when the flag equals the constant the guard compares against", which
        # holds for every value the constant could take, ``0x1`` included.
        st_flags = 0x40000000  # SF_DATALESS, from sys/stat.h
        st_blocks = 0
        st_size = 4096
        st_mode = real_stat(dataless).st_mode

    monkeypatch.setattr(Path, "stat", lambda self, **_: _Stat())
    monkeypatch.setattr(
        Path, "open", lambda *args, **kwargs: pytest.fail("the probe opened the file")
    )
    assert adopt_scan.probe_readability(dataless) is adopt_scan.Readability.ONLINE_ONLY


def test_a_file_that_merely_occupies_no_blocks_is_not_called_cloud_backed(cfg):
    """The block count answered a question it was never asked, twice.

    A SPARSE file reports a size and no blocks, and so does every file on a
    filesystem that does not populate the count at all, which is ordinary on
    network and FUSE mounts. Believing it there excludes an entire library and
    reports it as cloud backed, and there would be no readable file anywhere in
    the census to make that look wrong. An excluded track is one nobody decided
    about, so this is the more expensive direction to be wrong in.
    """
    music = Path(cfg.library.root) / "Music"
    sparse = music / "Sparse.flac"
    with sparse.open("wb") as handle:
        handle.truncate(1024 * 1024)
    assert sparse.stat().st_blocks == 0 and sparse.stat().st_size > 0, (
        "this platform allocated blocks for a sparse file, so the shape this "
        "test is about was never built"
    )
    assert adopt_scan.probe_readability(sparse) is adopt_scan.Readability.READABLE


def test_a_stale_placeholder_beside_a_readable_file_does_not_hide_it(cfg):
    """A stub is debris as often as it is evidence, and the file decides.

    A synchroniser's stub outlives the file coming back. Asking about it first
    reported a file that could be read in full as online-only, so adoption
    refused to touch a track sitting right there and named a remedy the person
    had already carried out.
    """
    music = Path(cfg.library.root) / "Music"
    present = music / "Back.flac"
    present.write_bytes(b"audio")
    (music / ".Back.flac.icloud").write_bytes(b"")
    assert adopt_scan.probe_readability(present) is adopt_scan.Readability.READABLE

    evicted = music / "Away.flac"
    (music / ".Away.flac.icloud").write_bytes(b"")
    assert adopt_scan.probe_readability(evicted) is adopt_scan.Readability.ONLINE_ONLY, (
        "the stub still has to settle the case it is the only evidence for"
    )


def test_the_probe_ITSELF_answers_rather_than_raising(cfg, tmp_path):
    """Totality is claimed as a property of THIS function, so drive this function.

    The census below catches the same two shapes independently, which meant the
    probe's own outer handlers could be deleted with the whole suite still green:
    a mutation battery found exactly that. A guard covered only by a second guard
    downstream is a guard whose removal nobody notices, and the docstring on
    ``probe_readability`` promises the property about itself.
    """
    music = Path(cfg.library.root) / "Music"
    locked = music / "locked"
    locked.mkdir()
    inside = locked / "Locked.flac"
    inside.write_bytes(b"audio")
    os.chmod(locked, 0o000)
    try:
        assert adopt_scan.probe_readability(inside) is adopt_scan.Readability.UNREADABLE
    finally:
        os.chmod(locked, 0o755)

    assert (
        adopt_scan.probe_readability(Path(f"{music}/bad\x00name.flac"))
        is adopt_scan.Readability.NOT_A_PATH
    )
    assert tmp_path


def test_the_census_survives_every_row_the_filesystem_refuses(cfg, declared, tmp_path):
    """Totality is a property of the PROBE, not of the inputs it is lucky with.

    The census is a generator, so a probe that raises does not misclassify one
    row, it ends the walk: every row after it is never produced, never counted,
    and reported missing by nothing. Two ordinary library shapes do exactly that.
    A directory with no execute bit makes ``Path.exists`` re-raise ``EACCES``, and
    a recorded path carrying a null byte makes ``stat`` raise ``ValueError``,
    which is not an ``OSError`` and is caught by nothing expecting one.
    """
    music = Path(cfg.library.root) / "Music"
    readable = music / "Fine.flac"
    readable.write_bytes(b"audio")
    locked = music / "locked"
    locked.mkdir()
    inside = locked / "Locked.flac"
    inside.write_bytes(b"audio")
    assert tmp_path

    rows = (
        [adopt_scan.CollectionRow(f"pre{i}", str(readable), "House", False) for i in range(9)]
        + [
            adopt_scan.CollectionRow("locked", str(inside), "House", False),
            adopt_scan.CollectionRow("null", f"{music}/bad\x00name.flac", "House", False),
        ]
        + [adopt_scan.CollectionRow(f"post{i}", str(readable), "House", False) for i in range(9)]
    )
    os.chmod(locked, 0o000)
    try:
        scanned = list(
            adopt_scan.scan_rows(rows, declared, root=cfg.library.root)
        )
    finally:
        os.chmod(locked, 0o755)

    assert len(scanned) == len(rows), (
        "the census stopped part way and every row after it is a track nobody "
        "decided about, with no count anywhere saying so"
    )
    found = {track.content_id: track.readability for track in scanned}
    assert found["locked"] is adopt_scan.Readability.UNREADABLE
    assert found["null"] is adopt_scan.Readability.NOT_A_PATH
    assert found["post8"] is adopt_scan.Readability.READABLE


def test_a_probe_of_the_callers_own_cannot_end_the_census_either(cfg, declared):
    """The probe is a PARAMETER, so its totality is somebody else's property."""
    music = Path(cfg.library.root) / "Music"
    readable = music / "Fine.flac"
    readable.write_bytes(b"audio")

    def hostile(path: Path) -> adopt_scan.Readability:
        if path.name == "Fine.flac":
            raise OSError("the volume went away mid-scan")
        return adopt_scan.Readability.READABLE

    rows = [adopt_scan.CollectionRow(f"c{i}", str(readable), "House", False) for i in range(5)]
    scanned = list(
        adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=hostile)
    )
    assert len(scanned) == 5
    assert {track.readability for track in scanned} == {adopt_scan.Readability.UNREADABLE}


@pytest.mark.parametrize("spelling", ["localhost", "empty-authority"])
def test_a_row_recorded_THE_WAY_REKORDBOX_RECORDS_ONE_is_adoptable(cfg, declared, spelling):
    """The census against the shape a real library holds, not the assumed one.

    rekordbox's ``Location`` column is a percent-encoded file URL, and
    ``resolve_recorded_path`` refuses anything that does not open with a slash,
    correctly, because a value that is not a path must not be guessed into one.
    Handed the raw column, every row in a real library came back ``not-a-path``,
    every one was excluded, and the plan carried the entire library in a category
    none of it belonged to.

    WHAT DID NOT CATCH THAT, and why this test is shaped the way it is.
    :func:`covers` compares content identifiers, so a plan filing every row under
    the wrong category satisfies "nothing fell out of the plan" exactly as well
    as a correct plan does. The arithmetic is a proof about PRESENCE, not about
    correctness, and every test around it built its rows from a bare filesystem
    path. Only the real recorded shape can see the difference, so this asserts
    the CATEGORY and the applicable count rather than the coverage.
    """
    music = Path(cfg.library.root) / "Music"
    present = music / "Recorded.flac"
    present.write_bytes(b"audio")
    _routable, genre = _bucket_and_genre(declared)
    recorded = (
        locations.location_url(present)
        if spelling == "localhost"
        else "file://" + str(present)
    )
    assert not recorded.startswith("/"), "the fixture built a path, not a location"

    rows = [adopt_scan.CollectionRow("c1", recorded, genre, False)]
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root))
    assert scanned[0].readability is adopt_scan.Readability.READABLE
    assert scanned[0].disposition is adopt_scan.Disposition.ROUTE
    assert scanned[0].path == str(present)

    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)
    assert len(plan.applicable()) == 1, (
        "the plan covers every row and can apply none of them, which is what a "
        "count-based proof cannot tell apart from a correct plan"
    )
    assert adopt_plan.covers(plan, scanned) == frozenset(), (
        "coverage was satisfied by the broken build too; it is asserted here "
        "only to show that it stays satisfied by the fixed one"
    )


def test_a_location_naming_another_host_is_reported_rather_than_guessed(cfg, declared):
    """The decoder refuses a remote authority, and the census must not die on it.

    A READABLE ROW SITS BESIDE IT ON PURPOSE. Against the pre-decode build this
    assertion passed for the wrong reason: every row classified ``not-a-path``
    back then, so the defect satisfied it. Requiring the sibling to come back
    ``readable`` is what makes this test about the remote authority rather than
    about a build in which nothing resolves at all.
    """
    music = Path(cfg.library.root) / "Music"
    present = music / "Local.flac"
    present.write_bytes(b"audio")
    rows = [
        adopt_scan.CollectionRow("remote", "file://elsewhere/Music/x.flac", "House", False),
        adopt_scan.CollectionRow("local", locations.location_url(present), "House", False),
    ]
    found = {
        track.content_id: track
        for track in adopt_scan.scan_rows(rows, declared, root=cfg.library.root)
    }
    assert found["remote"].readability is adopt_scan.Readability.NOT_A_PATH
    assert found["remote"].disposition is adopt_scan.Disposition.EXCLUDED
    assert found["local"].readability is adopt_scan.Readability.READABLE, (
        "every row came back not-a-path, so this test would pass against a build "
        "that resolves nothing at all"
    )


def test_a_row_whose_location_column_is_NULL_does_not_end_the_census(cfg, declared):
    """A null ``FolderPath`` is an ordinary rekordbox row.

    ``CollectionRow.recorded`` is annotated ``str`` and a database does not have
    to agree. The decoder asks a string method of whatever it is handed, so a
    None raised ``AttributeError`` out of the generator and took every later row
    with it: a two row census returned zero rows and raised. The resolver this
    replaced survived it, by coercing with ``str`` before testing for a leading
    slash, so this was a regression introduced one line above the probe that had
    just been hardened against exactly this class of failure.
    """
    music = Path(cfg.library.root) / "Music"
    present = music / "After.flac"
    present.write_bytes(b"audio")
    rows = [
        adopt_scan.CollectionRow("null", None, "House", False),  # type: ignore[arg-type]
        adopt_scan.CollectionRow("after", str(present), "House", False),
    ]
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root))
    assert len(scanned) == 2, "the census raised and every later row was lost"
    assert scanned[0].readability is adopt_scan.Readability.NOT_A_PATH
    assert scanned[0].disposition is adopt_scan.Disposition.EXCLUDED
    assert scanned[1].readability is adopt_scan.Readability.READABLE


def test_a_recorded_location_handed_over_as_a_Path_still_resolves(cfg, declared):
    """Refusing what can be coerced is the same defect as raising on it.

    Guarding the null column by demanding a ``str`` excluded every row in a
    library whose caller builds rows from :class:`~pathlib.Path` values, and named
    the category ``not-a-path``: the whole-library misclassification this module
    exists to prevent, arriving through the fix for it. The resolver this replaced
    coerced, so nothing about the annotation was ever load-bearing.
    """
    music = Path(cfg.library.root) / "Music"
    present = music / "AsPath.flac"
    present.write_bytes(b"audio")
    rows = [
        adopt_scan.CollectionRow("as-path", present, "House", False),  # type: ignore[arg-type]
        adopt_scan.CollectionRow("as-text", str(present), "House", False),
    ]
    found = {
        track.content_id: track
        for track in adopt_scan.scan_rows(rows, declared, root=cfg.library.root)
    }
    assert found["as-path"].readability is adopt_scan.Readability.READABLE
    assert found["as-path"].path == found["as-text"].path
    assert found["as-path"].readability is found["as-text"].readability


def test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped(cfg, declared):
    music = Path(cfg.library.root) / "Music"
    rows = [adopt_scan.CollectionRow("gone", str(music / "Gone.flac"), "House", False)]
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root))
    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)

    assert adopt_plan.covers(plan, scanned) == frozenset()
    entry = plan.entries[0]
    assert entry.disposition is adopt_scan.Disposition.EXCLUDED
    assert entry.category is adopt_scan.Readability.MISSING
    assert plan.applicable() == ()


def test_a_soft_deleted_row_is_not_proposed_for_adoption(cfg, declared):
    """A tombstone is a track the user removed on purpose. Adopting it puts it back."""
    music = Path(cfg.library.root) / "Music"
    rows = [
        adopt_scan.CollectionRow("live", str(music / "A.flac"), "House", False),
        adopt_scan.CollectionRow("dead", str(music / "B.flac"), "House", True),
    ]
    scanned = list(
        adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=_readable)
    )
    assert [track.content_id for track in scanned] == ["live"]


def test_a_row_that_cannot_report_its_soft_delete_marker_is_a_construction_error():
    """``deleted`` has no default, so a producer cannot supply the permissive one.

    U18 made this call for the tree writer's row record and U19 undid it through a
    defaulting accessor, which would have placed a deleted track and closed over
    it. The same field on the same kind of record is made the same way here.
    """
    with pytest.raises(TypeError):
        adopt_scan.CollectionRow("id", "/x/y.flac", "House")  # type: ignore[call-arg]


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 2: the third population has a declared disposition, always
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("genre", ["", "   ", None])
def test_a_blank_or_generic_genre_gets_a_disposition(declared, genre):
    disposition, bucket, _match = adopt_scan.classify_genre(declared, genre or "")
    assert disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert bucket == ""


def test_a_genre_the_taxonomy_calls_too_coarse_gets_a_disposition(declared):
    """Asked of the template rather than of a list here.

    ``is_too_coarse_as_source`` replaced two constants in the source system that
    always meant one thing and were never the same string, and asking the
    taxonomy is what lets a user's own template say what is too coarse for their
    library.
    """
    coarse = declared.fallback.too_coarse_as_source
    assert coarse, "the shipped template declares nothing too coarse to be a source"
    for value in coarse:
        disposition, bucket, _ = adopt_scan.classify_genre(declared, value)
        assert disposition is adopt_scan.Disposition.NEEDS_GENRE, value
        assert bucket == ""


def test_the_fallback_tier_is_never_accepted_as_an_adoption_answer(declared):
    """Approach point 2, and the defect it was caught as.

    The router is total and lands anything it cannot place in the declared
    fallback bucket, reporting that it did. For a single track that is correct.
    For an adoption pass it files thousands of tracks into one folder, in bulk,
    on approval given for a plan that looked complete, and a person can answer the
    genre question per track but nobody can un-answer it for four thousand.
    """
    resolution = adopt_scan.routing.resolve_bucket(declared, "a genre nobody declares")
    assert resolution.match is adopt_scan.routing.Match.FALLBACK
    assert resolution.bucket_id == declared.fallback.bucket

    disposition, bucket, _ = adopt_scan.classify_genre(declared, "a genre nobody declares")
    assert disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert bucket == ""


def test_the_plan_carries_every_scanned_row_whatever_happened_to_it(cfg, declared):
    """The strong form: a set comparison, not a count.

    A count would be satisfied by a plan that dropped one track and invented
    another, and the arithmetic that hid the original defect was exactly a number
    nobody was comparing against anything.
    """
    music = Path(cfg.library.root) / "Music"
    routable, genre = _bucket_and_genre(declared)
    rows = [
        adopt_scan.CollectionRow("ok", str(music / "A.flac"), genre, False),
        adopt_scan.CollectionRow("blank", str(music / "B.flac"), "", False),
        adopt_scan.CollectionRow("gone", str(music / "C.flac"), genre, False),
        adopt_scan.CollectionRow("stream", "provider:track:1", genre, False),
    ]

    def probe(path: Path) -> adopt_scan.Readability:
        if path.name == "C.flac":
            return adopt_scan.Readability.MISSING
        return adopt_scan.Readability.READABLE

    scanned = list(
        adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=probe)
    )
    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)

    assert adopt_plan.covers(plan, scanned) == frozenset()
    by_id = {entry.content_id: entry for entry in plan.entries}
    assert by_id["ok"].disposition is adopt_scan.Disposition.ROUTE
    assert by_id["ok"].bucket == routable
    assert by_id["blank"].disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert by_id["gone"].disposition is adopt_scan.Disposition.EXCLUDED
    assert by_id["stream"].disposition is adopt_scan.Disposition.EXCLUDED
    counts = plan.counts()
    assert counts[str(adopt_scan.Disposition.NEEDS_GENRE)] == 1


def test_a_track_needing_a_genre_becomes_a_review_item_not_a_file(cfg, declared, store):
    """R26's other half, and R12's rule about what an adjudication surface is."""
    music = Path(cfg.library.root) / "Music"
    rows = [adopt_scan.CollectionRow("blank", str(music / "A.flac"), "", False)]
    plan = _plan_of(cfg, declared, rows)

    offered = adopt_plan.offer_plan(store, plan, declared, handler_key=HANDLER)
    assert len(offered) == 1
    item = review.get(store, offered[0])
    assert item.queue == review.Queue.ADOPTION
    assert item.verdict is None
    assert item.handler_key == HANDLER
    assert {option.option_id for option in item.options} == set(declared.bucket_ids())

    # No comma separated file anywhere under the declared review directory.
    for current, _dirs, files in os.walk(config.state_path("review_queue", cfg)):
        for name in files:
            assert not name.endswith(".csv"), current


def test_re_offering_a_settled_question_does_not_reopen_it(cfg, declared, store):
    """The property that makes a plan resumable across sessions at all."""
    music = Path(cfg.library.root) / "Music"
    rows = [adopt_scan.CollectionRow("blank", str(music / "A.flac"), "", False)]
    plan = _plan_of(cfg, declared, rows)
    first = adopt_plan.offer_plan(store, plan, declared, handler_key=HANDLER)
    chosen = declared.bucket_ids()[0]
    review.resolve(
        store, first[0], review.Verdict.ACCEPTED, option=chosen, actor="tester"
    )

    second = adopt_plan.offer_plan(store, plan, declared, handler_key=HANDLER)
    assert second == first
    assert review.get(store, first[0]).verdict is review.Verdict.ACCEPTED
    assert review.count_unresolved(store, queue=review.Queue.ADOPTION) == 0


def test_an_answered_genre_question_turns_the_track_into_work(cfg, declared):
    music = Path(cfg.library.root) / "Music"
    routable, _genre = _bucket_and_genre(declared)
    rows = [adopt_scan.CollectionRow("blank", str(music / "A.flac"), "", False)]
    plan = _plan_of(cfg, declared, rows)
    assert plan.applicable() == ()

    answered = adopt_plan.with_verdicts(plan, {"blank": routable}, declared)
    assert len(answered.applicable()) == 1
    assert answered.applicable()[0].bucket == routable
    assert answered.digest() != plan.digest(), (
        "answering a question changed the plan and the digest did not move, so an "
        "approval given for the old one would apply the new one"
    )


def test_an_answer_naming_an_undeclared_bucket_is_ignored(cfg, declared):
    """It can only arrive from a verdict recorded against a template that moved.

    Inventing a folder from an identifier nobody declares is the failure
    ``routing_pass.destination`` refuses one layer down, and doing it here would
    put the folder in the user's library before that refusal was ever reached.
    """
    music = Path(cfg.library.root) / "Music"
    rows = [adopt_scan.CollectionRow("blank", str(music / "A.flac"), "", False)]
    plan = _plan_of(cfg, declared, rows)
    answered = adopt_plan.with_verdicts(plan, {"blank": "no_such_bucket"}, declared)
    assert answered.entries[0].disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert answered.applicable() == ()


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 6: a folder that is already there is surfaced, not merged
# ═══════════════════════════════════════════════════════════════════════════


def test_a_declared_folder_that_already_exists_is_surfaced(cfg, declared, store):
    music = Path(cfg.library.root) / "Music"
    routable, genre = _bucket_and_genre(declared)
    rows = [_row(cfg, "A.flac", genre, "a"), _row(cfg, "B.flac", genre, "b")]
    existing = [
        adopt_plan.ExistingFolder(
            node_id="node-41",
            display=declared.bucket(routable).display,
            content_ids=("a", "somebody-elses-track"),
        )
    ]
    plan = _plan_of(cfg, declared, rows, existing=existing)

    assert len(plan.collisions) == 1
    collision = plan.collisions[0]
    assert collision.node_id == "node-41"
    assert collision.bucket == routable
    assert collision.strangers == 1

    offered = adopt_plan.offer_plan(store, plan, declared, handler_key=HANDLER)
    item = review.get(store, offered[-1])
    assert item.kind == review.normalize_kind(adopt_plan.KIND_COLLISION)
    assert {option.option_id for option in item.options} == {
        adopt_plan.COLLISION_ADOPT,
        adopt_plan.COLLISION_SEPARATE,
    }
    assert music.exists()


def test_answering_keep_separate_actually_leaves_that_folder_alone(cfg, declared):
    """The question was asked and NOTHING READ THE ANSWER, which is worse than not asking.

    ``offer_plan`` offers ``adopt-existing`` and ``keep-separate``,
    ``with_verdicts`` handles genre answers only, ``apply_plan`` takes no
    verdicts, and both option identifiers appeared nowhere outside their own
    definition. So a plan with a real collision applied both tracks into that
    folder whatever the person chose, and somebody who answered "leave that
    folder alone" got the merge this module says it exists to prevent, with their
    name on the approval.
    """
    routable, genre = _bucket_and_genre(declared)
    rows = [_row(cfg, "A.flac", genre, "a"), _row(cfg, "B.flac", genre, "b")]
    existing = [
        adopt_plan.ExistingFolder(
            node_id="node-41",
            display=declared.bucket(routable).display,
            content_ids=("stranger-one", "stranger-two"),
        )
    ]
    plan = _plan_of(cfg, declared, rows, existing=existing)
    assert len(plan.applicable()) == 2 and len(plan.collisions) == 1

    left_alone = adopt_plan.with_collision_verdicts(
        plan, {"node-41": adopt_plan.COLLISION_SEPARATE}
    )
    assert left_alone.applicable() == (), (
        "the person said to leave the folder alone and adoption still has work "
        "queued for it"
    )
    assert {entry.disposition for entry in left_alone.entries} == {
        adopt_scan.Disposition.WITHHELD
    }
    assert adopt_plan.covers(left_alone, []) == frozenset()
    assert len(left_alone.entries) == len(plan.entries), (
        "a withheld track fell out of the plan instead of being carried with a "
        "name that says why"
    )
    assert left_alone.digest() != plan.digest(), (
        "answering the collision changed the plan and the digest did not move, "
        "so an approval given before the answer would apply the plan after it"
    )

    merged = adopt_plan.with_collision_verdicts(
        plan, {"node-41": adopt_plan.COLLISION_ADOPT}
    )
    assert len(merged.applicable()) == 2
    assert merged.digest() == plan.digest()

    # The identifier does not move, so changing an answer gives the work back
    # under the identifier the applied ledger already knows.
    assert {e.entry_id for e in left_alone.entries} == {e.entry_id for e in plan.entries}


def test_a_withheld_entry_is_never_written_by_an_apply(cfg, declared, tmp_path):
    """The verdict has to reach the writer, not just the report."""
    routable, genre = _bucket_and_genre(declared)
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    row = adopt_scan.CollectionRow("a", str(path), genre, False)
    scanned = list(adopt_scan.scan_rows([row], declared, root=tmp_path, probe=_readable))
    plan = adopt_plan.build_adoption_plan(
        scanned,
        declared,
        tree=TREE_ID,
        existing=[
            adopt_plan.ExistingFolder("node-41", declared.bucket(routable).display, ("x",))
        ],
    )
    withheld = adopt_plan.with_collision_verdicts(
        plan, {"node-41": adopt_plan.COLLISION_SEPARATE}
    )
    report = adopt_apply.apply_plan(
        cfg,
        withheld,
        declared,
        approval=adopt_approval.grant(withheld, actor="tester"),
        place=lambda *_: pytest.fail("a withheld entry reached the membership writer"),
        tag_value=lambda *_: "Adopted Genre",
    )
    assert report.applied == ()
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_folder_holding_only_what_the_plan_names_is_not_a_collision(cfg, declared):
    """P7. A guard that fires on the ordinary case is a guard people route around.

    Writing into a folder that already holds the tracks adoption is about to place
    is the feature working. Reporting it would train the reader to approve past
    this report, which is how the real one gets approved too.
    """
    routable, genre = _bucket_and_genre(declared)
    rows = [_row(cfg, "A.flac", genre, "a")]
    existing = [
        adopt_plan.ExistingFolder(
            node_id="node-41", display=declared.bucket(routable).display, content_ids=("a",)
        )
    ]
    assert _plan_of(cfg, declared, rows, existing=existing).collisions == ()


def test_a_collision_is_addressed_by_the_node_and_survives_a_rename(cfg, declared, store):
    """THE DEFECT U19 SHIPPED, one layer earlier, and it was blocking there.

    Its membership dedup targeted a destination's DISPLAY name, so a re-run after
    somebody renamed the folder in rekordbox found nothing under the new name,
    created the destination a second time, and filed one track in both. Here the
    same trap costs a person being asked a question they already answered, and
    the second answer proposes a second folder.

    So the review item's identity is the tree, the bucket, and the library node.
    Renaming the folder in rekordbox produces the SAME item, still carrying the
    verdict, with the new name refreshed in the payload where nothing keys on it.
    """
    routable, genre = _bucket_and_genre(declared)
    rows = [_row(cfg, "A.flac", genre, "a")]
    display = declared.bucket(routable).display
    before = adopt_plan.ExistingFolder("node-41", display, ("a", "stranger"))
    plan = _plan_of(cfg, declared, rows, existing=[before])
    first = adopt_plan.offer_plan(store, plan, declared, handler_key=HANDLER)
    review.resolve(
        store,
        first[-1],
        review.Verdict.ACCEPTED,
        option=adopt_plan.COLLISION_ADOPT,
        actor="tester",
    )

    # The collision is found through the taxonomy's display name, so a rename in
    # rekordbox alone makes the folder unfindable and the collision disappears.
    # What must NOT happen is a SECOND question about the same node, which is
    # what a name-keyed identity produces the moment the template is edited to
    # match the new name.
    renamed_declared = _taxonomy_with_bucket_display(declared, routable, "Renamed Shelf")
    after = adopt_plan.ExistingFolder("node-41", "Renamed Shelf", ("a", "stranger"))
    replanned = _plan_of(cfg, renamed_declared, rows, existing=[after])
    second = adopt_plan.offer_plan(replanned_store := store, replanned, renamed_declared, handler_key=HANDLER)

    assert second[-1] == first[-1], (
        "the renamed folder produced a second review item for one library node, "
        "so the person is asked again and the second answer proposes a duplicate"
    )
    settled = review.get(replanned_store, second[-1])
    assert settled.verdict is review.Verdict.ACCEPTED
    assert settled.payload["node_id"] == "node-41"
    # The payload of a SETTLED item is deliberately not refreshed by a re-offer,
    # so what is on record is what the person was looking at when they decided.
    # That is the queue's rule rather than this unit's, and it is asserted here
    # because a display name that quietly updated under a recorded verdict would
    # make the record say the decision was made about something it was not.
    assert settled.payload["display"] == display


def _taxonomy_with_bucket_display(declared, bucket_id: str, display: str):
    """The same template with one bucket renamed, REBUILT THROUGH THE LOADER.

    Through ``load_taxonomy`` over the shipped template's own text rather than by
    constructing a ``Taxonomy`` and patching a field. U18's review found exactly
    that second shape in a test: the object looked right, its four derived
    indexes were silently zeroed, and every lookup through it answered None while
    the test passed for the wrong reason.
    """
    import tomllib

    from cratekit.core.taxonomy import DEFAULT_TEMPLATE, load_taxonomy

    source = (SRC_ROOT / "cratekit" / "templates" / DEFAULT_TEMPLATE).read_text()
    data = tomllib.loads(source)
    old = declared.bucket(bucket_id).display
    for bucket in data["bucket"]:
        if bucket.get("id") == bucket_id:
            bucket["display"] = display
    assert old != display
    # The template is re-serialized through the loader's own parser rather than
    # by string replacement, so a display name that happens to appear elsewhere
    # in the document is not rewritten with it.
    import tomli_w

    return load_taxonomy(tomli_w.dumps(data))


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 4: R34. Nothing blanket applies a plan
# ═══════════════════════════════════════════════════════════════════════════


BLANKET_SHAPES = [
    True,
    1,
    "yes",
    "approve",
    {"approved": True},
    {"digest": "anything", "actor": "somebody", "option": "approve"},
    None,
]


@pytest.mark.parametrize("blanket", BLANKET_SHAPES, ids=lambda v: str(type(v).__name__) + str(v)[:12])
def test_no_blanket_affirmative_applies_a_plan(cfg, declared, blanket):
    """R34, checked at RUNTIME rather than in the type checker.

    ``require_approval`` takes ``object`` on purpose. The shapes it has to refuse
    are exactly the shapes a caller reaches for to get past it, and a signature
    that accepted ``Approval | None`` would put the refusal where it protects the
    author rather than the user.
    """
    routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    assert plan.applicable(), "the fixture built a plan with nothing to apply"

    with pytest.raises(CratekitError) as excinfo:
        adopt_apply.apply_plan(
            cfg,
            plan,
            declared,
            approval=blanket,
            place=lambda *_: pytest.fail("an unapproved plan reached the writer"),
        )
    assert excinfo.value.cause.reason == "decision-required"
    assert excinfo.value.cause.detail["gate"] == adopt_approval.APPROVAL_GATE
    assert not adopt_apply.path_for(cfg).exists(), (
        "a refused apply left a ledger behind, so the refusal had already "
        "written something"
    )
    assert routable


def test_an_approval_for_a_different_plan_is_refused(cfg, declared):
    routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    granted = adopt_approval.grant(plan, actor="tester")

    bigger = _plan_of(
        cfg, declared, [_row(cfg, "A.flac", genre, "a"), _row(cfg, "B.flac", genre, "b")]
    )
    with pytest.raises(CratekitError) as excinfo:
        adopt_apply.apply_plan(
            cfg,
            bigger,
            declared,
            approval=granted,
            place=lambda *_: pytest.fail("a stale approval reached the writer"),
        )
    assert excinfo.value.cause.reason == "decision-stale"
    assert excinfo.value.cause.detail["approved"] == granted.digest
    assert routable


def test_an_approval_with_no_actor_is_refused(cfg, declared):
    """R34's second half: each write session records WHICH actor asserted."""
    _routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    with pytest.raises(CratekitError) as excinfo:
        adopt_approval.grant(plan, actor="   ")
    assert excinfo.value.cause.reason == "decision-required"

    unattributed = adopt_approval.Approval(
        digest=plan.digest(), actor="", granted="2026-08-02T00:00:00+00:00"
    )
    with pytest.raises(CratekitError):
        adopt_approval.require_approval(plan, unattributed)


def test_a_recorded_answer_that_is_not_an_approval_applies_nothing(cfg, declared):
    _routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    declined = adopt_approval.Approval(
        digest=plan.digest(),
        actor="tester",
        granted="2026-08-02T00:00:00+00:00",
        option="abort",
    )
    with pytest.raises(CratekitError) as excinfo:
        adopt_approval.require_approval(plan, declined)
    assert excinfo.value.cause.reason == "decision-required"


# ── the source guard, run in BOTH directions ────────────────────────────────


def _reads_the_environment(source: str) -> list[str]:
    """Every place a source reads a process environment variable.

    Bound through the import graph rather than matched by bare name, which is the
    lesson U11 paid for: three countdown guards matched attribute NAMES with no
    binding to the module they were about, so a file that never touched the
    review queue satisfied all three. Here the same discipline means an object of
    somebody else's with a ``getenv`` method is not an answer, and
    ``import os as system`` is.
    """
    tree = ast.parse(source)
    modules: set[str] = set()
    symbols: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "os":
                    modules.add(alias.asname or "os")
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            for alias in node.names:
                if alias.name in {"environ", "getenv"}:
                    symbols.add(alias.asname or alias.name)

    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in {"environ", "getenv"}:
            value = node.value
            if isinstance(value, ast.Name) and value.id in modules:
                found.append(f"line {node.lineno}: {ast.unparse(node)}")
        elif isinstance(node, ast.Name) and node.id in symbols:
            found.append(f"line {node.lineno}: {node.id}")
    return found


ENVIRONMENT_EVASIONS = [
    "import os\nvalue = os.environ['CRATEKIT_APPROVE_EVERYTHING']\n",
    "import os as system\nvalue = system.getenv('CRATEKIT_APPROVE_EVERYTHING')\n",
    "from os import environ\nvalue = environ.get('CRATEKIT_APPROVE_EVERYTHING')\n",
    "from os import getenv as read\nvalue = read('CRATEKIT_APPROVE_EVERYTHING')\n",
]


@pytest.mark.parametrize("source", ENVIRONMENT_EVASIONS)
def test_the_environment_guard_bites_every_import_shape(source):
    """P7's half that keeps getting skipped: run the guard against the evasion.

    U11's armed comma-separated-writer guard was switched off by one keyword,
    ``import csv as spreadsheet``, because its self-test checked the two obvious
    import shapes and never the alias. Every shape the language offers is checked
    here, in both directions.
    """
    assert _reads_the_environment(source)


@pytest.mark.parametrize(
    "source",
    [
        "import os\npath = os.path.join('a', 'b')\n",
        "value = settings.environ\n",
        "# a comment about os.environ and getenv\n'a docstring naming os.environ'\n",
    ],
)
def test_the_environment_guard_stays_quiet_on_correct_code(source):
    """A guard that fires on correct code trains people to route around it (P7)."""
    assert not _reads_the_environment(source)


def test_no_module_in_the_adoption_package_reads_the_environment():
    """R34 as a structural property rather than a promise.

    An environment variable satisfies every gate at once and is invisible in the
    command somebody ran, which is why :class:`cratekit.cli.gates.Gates` has three
    sources and no fourth. This package must not acquire one by the back door.
    """
    offenders: dict[str, list[str]] = {}
    for path in sorted(ADOPT_ROOT.rglob("*.py")):
        found = _reads_the_environment(path.read_text())
        if found:
            offenders[path.name] = found
    assert not offenders, offenders


def test_the_adoption_package_writes_no_comma_separated_file():
    """R12: adjudication is a persisted review item, never a file to hand edit."""
    from tests._source_guards import constructs_a_csv_writer

    for path in sorted(ADOPT_ROOT.rglob("*.py")):
        assert not constructs_a_csv_writer(path.read_text()), path.name


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 3: applied thirty percent through, resumed from item thirty one
# ═══════════════════════════════════════════════════════════════════════════


def _hundred(cfg_value, declared_taxonomy) -> adopt_plan.AdoptionPlan:
    _routable, genre = _bucket_and_genre(declared_taxonomy)
    rows = [_row(cfg_value, f"Track {n:03d}.flac", genre, f"c{n:03d}") for n in range(1, 101)]
    return _plan_of(cfg_value, declared_taxonomy, rows)


def test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one(cfg, declared):
    """The brief's third scenario, driven through a real interruption.

    The first run raises out of the writer on the thirty-first entry, exactly as
    a killed process would leave it, and the second run starts there. What is
    asserted is the IDENTIFIERS, not a count: a count would be satisfied by a
    resume that skipped the wrong thirty.
    """
    plan = _hundred(cfg, declared)
    granted = adopt_approval.grant(plan, actor="tester")
    wrote: list[str] = []

    def place(entry, _folder, _sub):
        if len(wrote) == 30:
            # A KILL, not a refusal. A structured refusal is handled per entry
            # and reported, which is a different path; what the brief's scenario
            # describes is a run that stops existing partway through, so nothing
            # this module wrote gets a chance to tidy up after it.
            raise KeyboardInterrupt("the process died here")
        wrote.append(entry.entry_id)

    with pytest.raises(KeyboardInterrupt):
        adopt_apply.apply_plan(cfg, plan, declared, approval=granted, place=place)

    assert len(wrote) == 30
    ledger = adopt_apply.read(cfg)
    assert ledger.entry_ids() == frozenset(wrote)

    remaining = adopt_apply.outstanding(plan, ledger)
    assert remaining[0].ordinal == 31, (
        "the resume did not start at the entry after the last one that landed"
    )
    assert len(remaining) == 70

    resumed: list[str] = []
    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=granted,
        place=lambda entry, _f, _s: resumed.append(entry.entry_id),
    )
    assert report.resumed_at == 31
    assert len(report.applied) == 70
    assert len(report.already_applied) == 30
    assert set(wrote).isdisjoint(resumed), "a resumed run re-applied work that landed"
    assert adopt_apply.outstanding(plan, adopt_apply.read(cfg)) == ()


def test_a_second_run_over_a_finished_plan_writes_nothing(cfg, declared):
    plan = _hundred(cfg, declared)
    granted = adopt_approval.grant(plan, actor="tester")
    adopt_apply.apply_plan(cfg, plan, declared, approval=granted, place=lambda *_: None)

    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=granted,
        place=lambda *_: pytest.fail("a finished plan reached the writer again"),
    )
    assert report.applied == ()
    assert report.resumed_at is None
    assert len(report.already_applied) == 100


def test_the_ledger_is_marked_only_after_the_write(cfg, declared):
    """The order U19 established, and the one direction that is not recoverable.

    A mark that ran first suppresses the work on every later run while the
    library never received it. A mark that runs second costs a re-run at worst.
    """
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", _bucket_and_genre(declared)[1], "a")])
    granted = adopt_approval.grant(plan, actor="tester")
    seen: list[bool] = []

    def place(_entry, _folder, _sub):
        seen.append(adopt_apply.read(cfg).entry_ids() == frozenset())

    adopt_apply.apply_plan(cfg, plan, declared, approval=granted, place=place)
    assert seen == [True], "the entry was marked applied before it was written"


def test_a_failed_write_leaves_the_entry_outstanding(cfg, declared):
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", _bucket_and_genre(declared)[1], "a")])
    granted = adopt_approval.grant(plan, actor="tester")

    def place(_entry, _folder, _sub):
        raise adopt_apply.AppliedLedgerUnreadable(
            "the library refused", path=Path("/x"), remedy=Remedy.RUN_DOCTOR
        )

    report = adopt_apply.apply_plan(cfg, plan, declared, approval=granted, place=place)
    assert report.applied == ()
    assert len(report.failed) == 1
    assert adopt_apply.outstanding(plan, adopt_apply.read(cfg)) == plan.applicable()


def test_the_membership_mapping_resolves_display_names_at_write_time(cfg, declared):
    """R19: the record keys on identifiers and the names are resolved from the template.

    Renaming a bucket in the taxonomy between the plan and the apply changes where
    the tracks go and orphans nothing, which is only true because the plan stores
    no display name at all.
    """
    routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    entry = plan.applicable()[0]
    assert declared.bucket(routable).display not in (entry.bucket, entry.sub)

    mapping = adopt_apply.membership_plan(plan.applicable(), declared)
    assert list(mapping) == [
        adopt_apply.destination(declared, entry.bucket, entry.sub)
    ]
    assert list(mapping.values()) == [["a"]]

    renamed = _taxonomy_with_bucket_display(declared, routable, "Renamed Shelf")
    remapped = adopt_apply.membership_plan(plan.applicable(), renamed)
    assert list(remapped)[0][0] == "Renamed Shelf"


def test_an_entry_whose_destination_the_template_dropped_costs_one_entry(cfg, declared):
    """PER ENTRY, never out of the pass. U19 paid for this one.

    One stale sub identifier aborted a whole routing pass with a bare key error,
    which spent the remedy and placed nothing.
    """
    from dataclasses import replace

    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", _bucket_and_genre(declared)[1], "a")])
    broken = replace(plan.entries[0], sub="a_sub_nobody_declares")
    plan = adopt_plan.AdoptionPlan(tree=plan.tree, entries=(broken,))
    granted = adopt_approval.grant(plan, actor="tester")

    assert adopt_apply.membership_plan(plan.applicable(), declared) == {}
    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=granted,
        place=lambda *_: pytest.fail("an unresolvable destination reached the writer"),
    )
    assert report.applied == ()
    assert len(report.failed) == 1


def _plan_over_real_files(cfg_value, declared_taxonomy, tmp_path, suffixes):
    """A plan whose entries point at files that really exist, one per suffix."""
    _routable, genre = _bucket_and_genre(declared_taxonomy)
    rows = []
    for index, suffix in enumerate(suffixes):
        if suffix == ".aac":
            # A container this build has no verified handling for. Written as
            # bytes rather than encoded, because what matters is the suffix.
            path = tmp_path / f"track{index}.aac"
            path.write_bytes(b"not a container this module knows")
        else:
            path = _synth_in(tmp_path / f"t{index}", suffix)
            tags.write_genre(path, f"Original {index}")
        rows.append(adopt_scan.CollectionRow(f"c{index}", str(path), genre, False))
    scanned = list(
        adopt_scan.scan_rows(rows, declared_taxonomy, root=tmp_path, probe=_readable)
    )
    assert cfg_value is not None
    return adopt_plan.build_adoption_plan(scanned, declared_taxonomy, tree=TREE_ID)


def test_a_refusal_from_the_writer_rewrites_no_files_at_all(cfg, declared, tmp_path):
    """The gates in front of a destructive run are DOWNSTREAM of this write.

    With the tag write first, a systemic refusal raised inside ``place`` (a lock
    held elsewhere, an unanswered backup gate, a snapshot never verified) was
    caught per entry and the loop carried on, so six files came back
    ``applied=0 failed=6``, an empty applied ledger, zero memberships, and all
    six files on disk holding adoption's genre instead of their own. One refusal
    multiplied into one irreversible file write per entry in the plan.

    THE ORDERING IS THE FIX AND THIS ASSERTS IT: the recoverable write goes
    first, so no file is rewritten however many entries meet the same refusal.
    Round 2 also stopped the run on a scope wider than one item, which broke the
    per-track rule U19 paid for, so the count below is every entry rather than one.
    """
    plan = _plan_over_real_files(cfg, declared, tmp_path, [".flac"] * 6)
    assert len(plan.applicable()) == 6

    def refusing_place(*_args):
        raise cause.refuse(
            "decision-required", "the backup acknowledgment has not been answered"
        )

    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=refusing_place,
        tag_value=lambda *_: "Adopted Genre",
    )
    # THE FILES FIRST. The counts are the symptom; what the refusal cost is the
    # thing on disk that no snapshot and no re-import puts back.
    for index, entry in enumerate(plan.applicable()):
        assert tags.read_genre_from_file(Path(entry.path)) == f"Original {index}", (
            "a refused run rewrote the genre tag on a user's file, and it did it "
            "once per entry in the plan"
        )
    assert adopt_revert.read(cfg).snapshots == (), (
        "a refused run left revert records, so it had already touched files"
    )
    assert report.applied == ()
    assert adopt_apply.read(cfg).applied == ()
    # REPORTED ONCE PER ENTRY, and that is correct rather than tolerated. The
    # first fix broke the loop on a scope wider than one item, which ended the
    # pass on an ORDINARY per-track refusal too, because ``cause.refuse``
    # defaults to ``Scope.RUN``. Reporting a systemic refusal six times is noise
    # in a report; not attempting five entries is the failure U19 paid for.
    assert set(report.failed) == {entry.entry_id for entry in plan.applicable()}


def test_a_refusal_about_one_track_still_costs_only_that_track(cfg, declared, tmp_path):
    """The other direction, so the fix is not "stop on everything" (P7).

    WRITTEN THE WAY A CALLER ACTUALLY WRITES IT: a bare ``cause.refuse`` with no
    scope argument, which is every refusal in this repository, because
    ``cause.refuse`` DEFAULTS to ``Scope.RUN`` and nothing in ``cratekit.write``
    declares ``Scope.ITEM`` at all. An earlier version of this test passed
    ``scope=cause.Scope.ITEM`` explicitly and so agreed with the defect it was
    supposed to catch: it proved the loop kept going for a scope no caller ever
    sets, while the loop broke for the scope every caller does.

    On a six entry plan whose ``place`` refuses one row, the measured result was
    three ``place`` calls, two applied, and three entries never attempted at all.
    That is the per-track versus per-pass failure U19 paid for and the one
    ``membership_plan``'s docstring in this same module says it refuses to have.
    """
    plan = _plan_over_real_files(cfg, declared, tmp_path, [".flac"] * 6)
    refused = plan.applicable()[0].entry_id
    attempted: list[str] = []

    def place(entry, _folder, _sub):
        attempted.append(entry.entry_id)
        if entry.entry_id == refused:
            raise cause.refuse(
                "internal-error", "this one row has no collection entry"
            )

    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=place,
        tag_value=lambda *_: "Adopted Genre",
    )
    assert len(attempted) == 6, (
        f"only {len(attempted)} of 6 entries were attempted; one row's refusal "
        f"ended the pass"
    )
    assert len(report.applied) == 5 and list(report.failed) == [refused]
    for entry in plan.applicable():
        if entry.entry_id == refused:
            continue
        assert tags.read_genre_from_file(Path(entry.path)) == "Adopted Genre"


def test_a_track_DELETED_between_the_census_and_the_apply_costs_one_entry(
    cfg, declared, tmp_path
):
    """The ledger keys a record on the file's identity, so a vanished file cannot be recorded.

    ``identity_of`` stats the file, and a tag write with no record behind it is
    the one operation in this product that nothing can undo, so
    ``write_tag_with_record`` refuses rather than writing. That refusal has to
    cost exactly this entry, which is the per-track versus per-pass rule this
    package pays for everywhere else: unhandled, one track somebody deleted
    between the scan and the apply ended the whole run and every later entry was
    never attempted.
    """
    plan = _plan_over_real_files(cfg, declared, tmp_path, [".flac"] * 4)
    entries = plan.applicable()
    gone = entries[1]
    Path(gone.path).unlink()
    attempted: list[str] = []

    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=lambda entry, _f, _s: attempted.append(entry.entry_id),
        tag_value=lambda *_: "Adopted Genre",
    )
    assert len(attempted) == 4, (
        f"only {len(attempted)} of 4 entries were attempted; one deleted track "
        f"ended the pass"
    )
    assert list(report.failed) == [gone.entry_id], report.failed
    assert "cannot be identified on this machine" in report.failed[gone.entry_id]
    assert len(report.applied) == 3
    assert adopt_revert.read(cfg).snapshot(
        adopt_revert.identity_of(Path(entries[0].path)), "genre"
    ) is not None
    for entry in entries:
        if entry.entry_id == gone.entry_id:
            continue
        assert tags.read_genre_from_file(Path(entry.path)) == "Adopted Genre"


def test_a_record_is_never_written_for_a_file_that_cannot_be_identified(
    cfg, tmp_path
):
    """The refusal itself, and that it is a refusal rather than a fallback.

    Falling back to something derived from the path would put a second identity
    scheme back into one ledger beside the one that replaced it, which is the
    defect this round removed. So it raises, and it raises with a declared slug
    so a caller can tell it from any other failure.
    """
    missing = tmp_path / "not-here.flac"
    with pytest.raises(adopt_revert.AdoptedFileUnidentifiable) as refused:
        adopt_revert.write_tag_with_record(
            cfg, missing, field="genre", written="Adopted", entry_id="e1"
        )
    assert refused.value.cause.reason == "adoption-file-unidentifiable"
    assert REASONS["adoption-file-unidentifiable"] is ExitCode.PRECONDITION
    assert refused.value.cause.scope is cause.Scope.ITEM
    assert adopt_revert.read(cfg).snapshots == (), (
        "a record was written for a file this build cannot identify, so a later "
        "revert has an entry it can never match to anything"
    )


def test_a_container_this_build_cannot_write_costs_one_entry_not_the_run(
    cfg, declared, tmp_path
):
    """``write_tags`` raises ``UnsupportedContainer`` from OUTSIDE its own try.

    So one ``.aac`` in a plan raised out of ``apply_plan`` itself: no report was
    returned, the entries after it were never attempted, and every re-run died on
    the same file, so the plan could never complete. That is the per-pass failure
    ``membership_plan``'s own docstring says it refuses to have. It also left a
    revert record for a file whose tag was never written, which is a promise to
    restore something nothing ever changed.
    """
    plan = _plan_over_real_files(
        cfg, declared, tmp_path, [".flac", ".flac", ".aac", ".flac"]
    )
    awkward = next(e for e in plan.applicable() if e.path.endswith(".aac"))
    placed: list[str] = []
    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=lambda entry, *_: placed.append(entry.entry_id),
        tag_value=lambda *_: "Adopted Genre",
    )
    assert len(report.applied) == 3 and list(report.failed) == [awkward.entry_id]
    assert not any(
        record.path.endswith(".aac") for record in adopt_revert.read(cfg).snapshots
    ), "a revert record was left for a file whose tag was never written"

    # AND IT NEVER RECEIVED A MEMBERSHIP EITHER. Asking about the container after
    # ``place`` fixed the abort and bought a second problem: the entry got its
    # playlist row, was then failed, and could never reach applied, so every
    # re-run placed it again and re-reported the same failure with nothing to
    # acknowledge. The question is asked before anything happens for the entry.
    assert awkward.entry_id not in placed, (
        "the entry this build cannot finish still had its membership written, so "
        "every re-run writes it again"
    )
    assert len(placed) == 3, (
        "3 is the full complement here: the .aac is refused before place, so "
        "every entry this build can finish was attempted"
    )

    second = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=lambda entry, *_: placed.append(entry.entry_id),
        tag_value=lambda *_: "Adopted Genre",
    )
    assert len(second.already_applied) == 3, "the plan can never finish"
    assert placed.count(awkward.entry_id) == 0, "the re-run placed it a second time"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 5: a tag write is reverted EXACTLY
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tag_write_is_reverted_exactly(cfg, tmp_path):
    """The value that was there before comes back, byte for byte.

    THROUGH THE COMPOSED CALL, which is what ``apply_plan`` uses and the only one
    that stamps the record. Taking the record half and writing separately leaves
    the record unstamped, and an unstamped record now refuses rather than
    accepting whatever is at the path.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    assert tags.read_genre_from_file(path) == "Adopted Genre"

    report = adopt_revert.revert_tags(cfg)
    assert report.restored == ((str(path), "genre"),)
    assert report.failed == {}
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert adopt_revert.read(cfg).snapshots == ()


def test_an_absent_tag_is_reverted_to_ABSENT_and_not_to_an_empty_string(cfg, tmp_path):
    """"Exactly" includes absence, and the tag writer cannot express it.

    ``write_tags`` skips a None on purpose, so handing it the field with a None
    writes nothing and returns True: a restore that did not happen, reported as
    one that did. Writing an empty string instead leaves a tag the user never had.
    """
    path = _synth(tmp_path, ".flac")
    assert tags.read_genre_from_file(path) is None

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    adopt_revert.revert_tags(cfg)
    assert tags.read_genre_from_file(path) is None


def test_the_original_is_recorded_before_the_file_is_touched(cfg, declared, tmp_path):
    """The seam where the reverse order loses a value nothing can put back."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _routable, genre = _bucket_and_genre(declared)
    row = adopt_scan.CollectionRow(str(path), str(path), genre, False)
    scanned = list(
        adopt_scan.scan_rows([row], declared, root=tmp_path, probe=_readable)
    )
    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)
    granted = adopt_approval.grant(plan, actor="tester")

    adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=granted,
        place=lambda *_: None,
        tag_value=lambda entry, dec: dec.bucket(entry.bucket).display,
    )
    recorded = adopt_revert.read(cfg).snapshots
    assert len(recorded) == 1
    assert recorded[0].original == ("Original Genre",)
    assert tags.read_genre_from_file(path) == declared.bucket(plan.applicable()[0].bucket).display

    adopt_revert.revert_tags(cfg)
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_re_run_after_a_crash_never_overwrites_the_recorded_original(cfg, tmp_path):
    """The crash between the tag write and the applied record, and why it is safe.

    The re-run writes the same tag again. Refreshing the record here would store
    the value adoption just wrote as the original, and the revert would then
    faithfully restore the thing it was supposed to undo. First write wins.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre"
    )

    again, _landed = adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre"
    )
    assert again.original == ("Original Genre",)
    assert len(adopt_revert.read(cfg).snapshots) == 1
    adopt_revert.revert_tags(cfg)
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_no_tag_is_written_unless_the_caller_asks_for_one(cfg, declared, tmp_path):
    """There is no default that writes. It is the one operation no restore undoes."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    row = adopt_scan.CollectionRow(str(path), str(path), _bucket_and_genre(declared)[1], False)
    scanned = list(adopt_scan.scan_rows([row], declared, root=tmp_path, probe=_readable))
    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)

    adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=lambda *_: None,
    )
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert adopt_revert.read(cfg).snapshots == ()


def test_two_fields_on_one_file_keep_two_records(cfg, tmp_path):
    """A ledger keyed on the file alone restores one field and keeps the other's new value.

    THE SUBJECT IS THE KEY AND NOTHING ELSE, so both records are overridden by
    name. Two fields on one file is the second instance of the wall in the residual
    titled "the adoption revert cannot recognize its own file after another
    Cratekit write": whichever
    field is written first has its digest invalidated by the second write, so the
    guard refuses it on every pass. Reverting without the override here would
    measure the guard rather than the keying, and would go green for the wrong
    reason the day the keying broke.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_tags(path, {"genre": "Original Genre", "title": "Original Title"})
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="New Genre")
    adopt_revert.snapshot_before_write(cfg, path, field="title", written="New Title")
    tags.write_tags(path, {"genre": "New Genre", "title": "New Title"})

    both = [(str(path), "genre"), (str(path), "title")]
    report = adopt_revert.revert_tags(cfg, force=both)
    assert report.failed == {}, report.failed
    assert sorted(report.restored) == sorted(both)
    assert tags.read_tag(path, "genre") == "Original Genre"
    assert tags.read_tag(path, "title") == "Original Title"


def test_one_file_in_two_composition_forms_is_one_record(cfg, tmp_path):
    """The primitive U31 exists for, and the cost of not using it here.

    A ledger keyed on the raw string holds two records for one accented filename,
    so a revert restores one of them and reports both done.

    DRIVEN THROUGH THE LEDGER rather than asserted about an identifier function.
    The previous version compared ``file_id`` of two strings for a file that did
    not exist, which is a statement about a hash and says nothing about what the
    ledger does with two adoptions of one file. Both spellings are written
    through the real writer here, and the assertion is the record count.
    """
    assert COMPOSED != DECOMPOSED
    directory = tmp_path / "accented"
    directory.mkdir()
    composed = _synth(directory, ".flac")
    composed = composed.rename(directory / COMPOSED)
    tags.write_genre(composed, "User Genre")
    decomposed = directory / DECOMPOSED

    adopt_revert.write_tag_with_record(
        cfg, composed, field="genre", written="Adopted", entry_id="e1"
    )
    adopt_revert.write_tag_with_record(
        cfg, decomposed, field="genre", written="Adopted", entry_id="e2"
    )

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.path for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)


def test_one_file_under_TWO_HARD_LINKS_is_one_record(cfg, tmp_path):
    """Two names, one inode, and the ledger used to hold two originals for it.

    The second record's ``original`` was ``("Adopted Bucket",)``, which is the
    value adoption itself had just written through the first name, because two
    path digests are two identities and first-write-wins never engaged between
    them. The revert then restored the real original through one record and
    offered to overwrite it with adoption's value through the other.

    Driven with ``os.link`` on real files and the real writer.
    """
    first = _synth(tmp_path, ".flac")
    tags.write_genre(first, "User Genre")
    second = tmp_path / "second-name.flac"
    os.link(first, second)
    assert first.stat().st_ino == second.stat().st_ino

    adopt_revert.write_tag_with_record(
        cfg, first, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    adopt_revert.write_tag_with_record(
        cfg, second, field="genre", written="Adopted Bucket", entry_id="e2"
    )

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.path, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",), (
        "the second record recorded adoption's own value as the original, so the "
        "user's genre is now in no file and no record"
    )
    assert ledger.snapshots[0].path == str(first), (
        "the recorded address was moved to the second name for no reason. A "
        "record's path is only ever corrected when the recorded one no longer "
        "resolves to this file, and this one resolves perfectly well; moving it "
        "on any weaker trigger is the line that handed one file's record to "
        "another file on a volume that recycles inode numbers"
    )
    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(first) == "User Genre"


def test_TWO_CASE_SPELLINGS_are_one_record_or_two_exactly_as_the_VOLUME_says(
    cfg, tmp_path
):
    """The defect on the volume format this product targets, and its mirror.

    ``Song.flac`` and ``song.flac`` are ONE file on a case insensitive volume,
    which is the APFS default, and they are two path digests, so the ledger held
    two records and the second one's "original" was the value adoption itself had
    written.

    THE FIX IS NOT TO LOWERCASE THE PATH, and this test is written to fail if
    anybody does. Case insensitivity is a property of the VOLUME rather than of
    the string: on a case sensitive volume the two names are two real files, each
    with its own original, and folding them into one record is the same defect
    pointed the other way. So the volume is ASKED, and the expected record count
    is whatever the volume's own answer implies. Both branches are real
    assertions and neither is a skip.
    """
    upper = tmp_path / "SongZero.flac"
    _synth(tmp_path, ".flac").rename(upper)
    lower = tmp_path / "songzero.flac"
    one_file = lower.exists()
    if not one_file:
        _synth_in(tmp_path / "src", ".flac").rename(lower)
        tags.write_genre(lower, "Lower Genre")
    tags.write_genre(upper, "Upper Genre")

    adopt_revert.write_tag_with_record(
        cfg, upper, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    adopt_revert.write_tag_with_record(
        cfg, lower, field="genre", written="Adopted Bucket", entry_id="e2"
    )

    originals = {entry.original for entry in adopt_revert.read(cfg).snapshots}
    if one_file:
        assert originals == {("Upper Genre",)}, originals
        assert adopt_revert.revert_tags(cfg).failed == {}
        assert tags.read_genre_from_file(upper) == "Upper Genre"
    else:
        assert originals == {("Upper Genre",), ("Lower Genre",)}, originals


def test_TWO_VOLUMES_that_allocate_the_SAME_INODE_NUMBER_stay_two_records(
    cfg, tmp_path
):
    """An inode number is unique to a volume and to nothing wider than that.

    Every filesystem numbers its own inodes from its own counter, so two volumes
    holding a track each will hand out the same low numbers as a matter of
    course, and a DJ library spread over an internal disk and an external drive
    is the ordinary case rather than a contrived one. An identity of the inode
    alone would merge two unrelated tracks into one record and lose one of their
    originals, which is the same defect the path digest had pointed the other
    way.

    A SECOND VOLUME IS SIMULATED IN ``stat`` rather than mounted, because a test
    cannot mount one. What is faked is the pair the identity is built from and
    nothing else, so the collision it produces is exactly the collision a real
    second volume produces.
    """
    first = _synth_in(tmp_path / "internal", ".flac")
    second = _synth_in(tmp_path / "external", ".flac")
    tags.write_genre(first, "Internal Genre")
    tags.write_genre(second, "External Genre")
    real_stat = Path.stat
    shared = real_stat(first).st_ino

    class _OnAnotherVolume:
        def __init__(self, info):
            self._info = info

        def __getattr__(self, name):
            return getattr(self._info, name)

        st_dev = 0xDEAD
        st_ino = shared

    def elsewhere(self, *args, **kwargs):
        info = real_stat(self, *args, **kwargs)
        return _OnAnotherVolume(info) if self == second else info

    Path.stat = elsewhere
    try:
        adopt_revert.write_tag_with_record(
            cfg, first, field="genre", written="Adopted Bucket", entry_id="e1"
        )
        adopt_revert.write_tag_with_record(
            cfg, second, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    finally:
        Path.stat = real_stat

    originals = {entry.original for entry in adopt_revert.read(cfg).snapshots}
    assert originals == {("Internal Genre",), ("External Genre",)}, originals


def test_a_file_RENAMED_between_two_adoptions_is_still_one_record(cfg, tmp_path):
    """The third spelling of one file, and the one the path digest never saw.

    A rename is the same inode under a new name, so a ledger keyed on the path
    wrote a second record on the next adoption and stored adoption's own value as
    the original. The recorded path is refreshed to the new name at the same
    time, because the path is the revert's only address for the file.
    """
    before = _synth(tmp_path, ".flac")
    tags.write_genre(before, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, before, field="genre", written="Adopted", entry_id="e1"
    )
    after = tmp_path / "renamed.flac"
    before.rename(after)
    adopt_revert.write_tag_with_record(
        cfg, after, field="genre", written="Adopted", entry_id="e2"
    )

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.path for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].path == str(after), (
        "the record still points at a name that is not there, so the revert has "
        "no address for the file it holds the only copy of the original for"
    )
    assert adopt_revert.revert_tags(cfg).failed == {}
    assert tags.read_genre_from_file(after) == "User Genre"


def test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled(
    cfg, tmp_path
):
    """An upgrade must not be a second identity for a file that already has one.

    Every ledger on disk today is keyed by a truncated digest of the path. A
    build that only looked for the new identity would find nothing, write a
    second record, and store adoption's own value as the original, which is the
    same data loss arriving through the upgrade rather than through a hardlink.

    THE LEGACY KEY IS SPELLED HERE from the width constant's own value rather
    than read off the module, because a test that derives the key the code
    derives passes for any width either of them takes.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    legacy = hashlib.sha256(
        locations.location_to_path(str(path)).encode("utf-8")
    ).hexdigest()[:24]
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(
            {
                "schema_version": adopt_revert.SCHEMA_VERSION,
                "snapshots": [
                    {
                        "file": legacy,
                        "field": "genre",
                        "path": str(path),
                        "original": ["User Genre"],
                        "written": "Adopted",
                        "recorded": "2026-08-03T00:00:00+00:00",
                        "entry": "e0",
                        "entries": ["e0"],
                    }
                ],
            }
        )
    )
    assert adopt_revert.read(cfg).snapshots[0].file == legacy

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.file for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].file == adopt_revert.identity_of(path)
    assert ledger.snapshots[0].written_by("e0")
    assert ledger.snapshots[0].written_by("e1")


def test_a_legacy_record_that_is_the_only_one_for_its_file_still_reverts(
    cfg, tmp_path
):
    """The direction an over-tightened identity check would have broken.

    A ledger nobody re-adopts through never reaches the migration, so its records
    keep the old key forever and every one of them still has to spend. One record
    for one file is unambiguous however it is keyed, which is why the ambiguity
    refusal is about GROUPS of records rather than about the scheme.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Adopted")
    legacy = hashlib.sha256(
        locations.location_to_path(str(path)).encode("utf-8")
    ).hexdigest()[:24]
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(
            {
                "schema_version": adopt_revert.SCHEMA_VERSION,
                "snapshots": [
                    {
                        "file": legacy,
                        "field": "genre",
                        "path": str(path),
                        "original": ["User Genre"],
                        "written": "Adopted",
                        "recorded": "2026-08-03T00:00:00+00:00",
                        "size": path.stat().st_size,
                        "mtime_ns": path.stat().st_mtime_ns,
                        "digest": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "digest_state": "recorded",
                    }
                ],
            }
        )
    )
    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "User Genre"


# ═══════════════════════════════════════════════════════════════════════════
# The identity is a CORROBORATION, and every disagreement is a refusal
# ═══════════════════════════════════════════════════════════════════════════


class _Renumbered:
    """One file's ``stat`` with the volume and inode a filesystem event moved.

    WHAT IS SUBSTITUTED IS THE PAIR THE IDENTITY IS BUILT FROM AND NOTHING ELSE,
    which is the convention the two-volumes test above already established. Size,
    mode and time come through untouched, so the collision or the move this
    produces is exactly the one the real event produces. A test cannot mount a
    FAT volume, unmount it and mount it again; it can present the two numbers
    that come back when it does.
    """

    def __init__(self, info, *, st_dev=None, st_ino=None):
        self._info = info
        self._dev = info.st_dev if st_dev is None else st_dev
        self._ino = info.st_ino if st_ino is None else st_ino

    def __getattr__(self, name):
        return getattr(self._info, name)

    @property
    def st_dev(self):
        return self._dev

    @property
    def st_ino(self):
        return self._ino


def _stat_reporting(monkeypatch, target: Path, **numbers):
    """Make ``target`` and nothing else report the volume and inode given."""
    real_stat = Path.stat

    def renumbered(self, *args, **kwargs):
        info = real_stat(self, *args, **kwargs)
        if self == target:
            return _Renumbered(info, **numbers)
        return info

    monkeypatch.setattr(Path, "stat", renumbered)


def test_a_RECYCLED_INODE_NUMBER_never_hands_one_files_record_to_another(
    cfg, tmp_path, monkeypatch
):
    """The defect the previous round shipped, driven end to end.

    An inode number is REUSED once the file holding it is deleted. Reproduced
    directly on a real MS-DOS FAT image, which is the format of every rekordbox
    export drive: a file at ``st_ino`` 9, deleted, and the next file created on
    that image came back as ``st_ino`` 9.

    Against the code, the previous build did this. Track A was adopted, its
    record keyed to A's volume and inode with A's genre as the original. A was
    deleted. Track B, a different recording with its own genre, inherited the
    number. Adopting B found A's record by the live identity, found A's path no
    longer stat'd, and REWROTE the record's path to B's. The stamp then wrote B's
    digest into A's record, so at revert the guard compared B against B, accepted,
    wrote A's original onto B, dropped the record and reported the pass clean. B's
    own genre was then in no file and no record.

    So the collision refuses. Nothing is written to B, B keeps its own value, and
    the record still says what it is about.
    """
    first = _synth_in(tmp_path / "a", ".flac")
    tags.write_genre(first, "Real Genre A")
    adopt_revert.write_tag_with_record(
        cfg, first, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.original == ("Real Genre A",)

    second = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(second, "Real Genre B")
    recycled = first.stat().st_ino
    first.unlink()
    _stat_reporting(monkeypatch, second, st_dev=held_dev(held), st_ino=recycled)
    assert adopt_revert.identity_of(second) == held.file

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        adopt_revert.write_tag_with_record(
            cfg, second, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert "inode number is REUSED" in refused.value.cause.message
    assert refused.value.cause.remediation.remedy is Remedy.RUN_DOCTOR

    assert tags.read_genre_from_file(second) == "Real Genre B", (
        "adoption wrote to a file whose original it had not recorded, which is "
        "the one act this product cannot undo"
    )
    assert adopt_revert.read(cfg).snapshots == (held,), (
        "the record moved, so one file's original is now filed under another "
        "file's name"
    )

    # AND THE REVERT CANNOT REACH B EITHER. The record still names A, which is
    # gone, so it is reported as gone rather than spent on whatever inherited its
    # number.
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), report.restored
    assert report.failed == {(str(first), "genre"): "the file is no longer there"}
    assert tags.read_genre_from_file(second) == "Real Genre B"


def held_dev(record) -> int:
    """The volume number a ``dev-ino`` record is keyed to."""
    return int(record.file.split(":")[1])


def test_a_recorded_path_is_NEVER_REFRESHED_to_a_DIFFERENT_files_path(
    cfg, tmp_path, monkeypatch
):
    """The one line that turned a collision into a data loss, pinned on its own.

    The collision above is survivable; what made it unrecoverable is that the
    record's own contradictory evidence was ERASED. ``existing.path`` named a file
    that no longer stat'd, so it was rewritten to the file in hand, and after that
    nothing anywhere could tell that two different files had been involved.

    So this asserts the record's address, not the report. Whatever the refusal
    says, the path in the ledger must still name the file the record is about.
    """
    first = _synth_in(tmp_path / "a", ".flac")
    tags.write_genre(first, "Real Genre A")
    adopt_revert.write_tag_with_record(
        cfg, first, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]

    second = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(second, "Real Genre B")
    recycled = first.stat().st_ino
    first.unlink()
    _stat_reporting(monkeypatch, second, st_dev=held_dev(held), st_ino=recycled)

    with pytest.raises(adopt_revert.RecordCannotBeMatched):
        adopt_revert.write_tag_with_record(
            cfg, second, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert adopt_revert.read(cfg).snapshots[0].path == str(first), (
        "the recorded path was refreshed to a different file's path, which "
        "destroys the only surviving evidence that they are different files"
    )
    assert adopt_revert.read(cfg).snapshots[0].file == held.file
    assert adopt_revert.read(cfg).snapshots[0].original == ("Real Genre A",)


def test_an_os_replace_SAVE_does_not_produce_a_SECOND_record(cfg, tmp_path):
    """The inode moves for a file nobody replaced, and every tagger does it.

    Measured on APFS: a save that writes a temporary file and renames it over the
    original moved ``st_ino`` 253021801 to 253021808 at the same path on the same
    volume. That is how mutagen-based taggers save, how Phillip's own tagging
    workflow saves, and how ``config.atomic_write_bytes`` in this repository
    saves. Keyed on the inode alone, the next adoption of that file found nothing,
    wrote a SECOND record, and stored the value adoption itself had written as the
    original.

    The bytes are asked and they do not answer, because the save rewrote them, so
    this refuses rather than filing a second original. The refusal costs one
    entry of one apply; the second record cost the only copy of a value.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    before = path.stat().st_ino

    saving = tmp_path / "saving.flac"
    saving.write_bytes(path.read_bytes())
    tags.write_tags(saving, {"title": "Retagged Elsewhere"})
    os.replace(saving, path)
    assert path.stat().st_ino != before, "the fixture did not move the inode"

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert "renames it over the original" in refused.value.cause.message

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.file, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",), (
        "the second record recorded adoption's own value as the original"
    )


@pytest.mark.parametrize(
    "moved",
    [
        pytest.param({"st_ino": 7}, id="inode-renumbered"),
        pytest.param({"st_dev": 16777240}, id="mounted-in-another-order"),
        pytest.param({"st_dev": 16777240, "st_ino": 7}, id="both"),
    ],
)
def test_a_REMOUNT_does_not_produce_a_SECOND_record(cfg, tmp_path, monkeypatch, moved):
    """Both halves of the pair move for an untouched file, and all three were measured.

    A FAT volume detached and reattached renumbered an untouched file from
    ``st_ino`` 18446744073709551613 to 7. Detaching two images and reattaching
    them in the opposite order moved the same file from ``st_dev`` 16777241 to
    16777240. Neither event touched a byte, and under an identity of the pair
    alone each of them produced a second record whose original was adoption's own
    value.

    Here the bytes DO answer, because nothing rewrote them, so the record is
    found, re-keyed to the numbers the file has now, and its original is kept.
    That is the difference between this and the save above: the same divergence,
    settled by the same evidence, arriving at opposite answers because the
    evidence differs.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    first = adopt_revert.read(cfg).snapshots[0]

    _stat_reporting(monkeypatch, path, **moved)
    assert adopt_revert.identity_of(path) != first.file, "the fixture moved nothing"
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
    )

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.file, entry.original) for entry in ledger.snapshots
    ]
    settled = ledger.snapshots[0]
    assert settled.original == ("User Genre",)
    assert settled.file == adopt_revert.identity_of(path), (
        "the record kept a key naming numbers this file no longer has, so the "
        "next adoption writes a second record beside it"
    )
    assert settled.path == str(path)
    assert settled.written_by("e1") and settled.written_by("e2")


def test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled(cfg, tmp_path):
    """The rename is one of the three spellings this whole round exists to handle.

    A legacy record is keyed by a digest of the path it was written for, and the
    lookup hashes the path in hand, so after a rename the key can never be found.
    Driven: the next adoption wrote a second record, and the revert then restored
    ``('After.flac', 'genre')`` to ADOPTION'S OWN VALUE while failing
    ``Before.flac`` as no longer there and reporting the pass otherwise clean.

    Neither address survives a rename, so the BYTES are what finds it. The record
    is stamped from what adoption left, the renamed file still holds exactly that,
    and no other stranded record was stamped from those bytes.
    """
    before = _synth(tmp_path, ".flac")
    tags.write_genre(before, "Adopted Bucket")
    _legacy_ledger(
        cfg, (before, "User Genre", hashlib.sha256(before.read_bytes()).hexdigest())
    )
    assert len(adopt_revert.read(cfg).snapshots) == 1

    after = tmp_path / "renamed.flac"
    before.rename(after)
    adopt_revert.write_tag_with_record(
        cfg, after, field="genre", written="Adopted Bucket", entry_id="e1"
    )

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.file, entry.path, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",), (
        "the second record stored adoption's own value as the original, so the "
        "user's genre is now in no file and no record"
    )
    assert ledger.snapshots[0].path == str(after)
    assert ledger.snapshots[0].file == adopt_revert.identity_of(after)

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(after) == "User Genre"


def test_TWO_RECORDS_claiming_one_file_by_DIFFERENT_evidence_refuse(cfg, tmp_path):
    """A ledger that contradicts itself is never resolved by preferring one claim.

    One record is keyed to the volume and inode this file has; a different record
    carries its path. Both cannot be about it. Preferring either is a guess about
    which of two originals a later revert writes onto a user's audio, and the
    honest answer is that nothing here knows.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    stray = dict(document["snapshots"][0])
    stray["file"] = "c" * 24
    stray["original"] = ["Some Other Original"]
    document["snapshots"][0]["path"] = str(tmp_path / "elsewhere.flac")
    document["snapshots"].append(stray)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    assert len(adopt_revert.read(cfg).snapshots) == 2

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert "claimed by two different records" in refused.value.cause.message
    assert len(adopt_revert.read(cfg).snapshots) == 2


def test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING(cfg, tmp_path, monkeypatch):
    """The corroboration is paid for only where a claim actually diverges.

    Reading the file to settle a disagreement is right; reading it when there is
    no disagreement is a whole-file hash per track on the one pass that touches
    every track in the library. So the common paths are asserted to perform ZERO
    reads: a first adoption, where no record claims the file, and an ordinary
    re-run, where the identity and the path claim it together.

    THE SECOND FILE IS THE POINT, and this test did not have one for a round. It
    adopted exactly ONE file, so the ledger it adopted into was EMPTY, and an
    empty ledger has no candidate to search by bytes whatever the search costs. A
    test named for the first adoption OF A LIBRARY has to put a second file into a
    ledger that already holds a stamped record, because that is where round 7 hid
    a whole-file hash per track: the candidate filter read the file first and
    discarded the candidates afterwards.
    """
    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    monkeypatch.setattr(
        adopt_revert, "digest_of", lambda p, **kw: (reads.append(p), real_digest(p))[1]
    )
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    # One read, and it is the stamp AFTER the write rather than a lookup.
    assert reads == [path], reads

    reads.clear()
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
    )
    assert reads == [path], (
        f"a re-run whose identity and path agree read the file to decide "
        f"something that was not in doubt, reads={reads}"
    )
    assert len(adopt_revert.read(cfg).snapshots) == 1

    # A SECOND FILE, INTO A LEDGER THAT ALREADY HOLDS A STAMPED RECORD.
    second = _synth_in(tmp_path / "second", ".flac")
    tags.write_genre(second, "Another User Genre")
    reads.clear()
    adopt_revert.write_tag_with_record(
        cfg, second, field="genre", written="Adopted Bucket", entry_id="e3"
    )
    assert reads == [second], (
        f"the second file into a non-empty ledger was hashed to look itself up "
        f"and then hashed again to stamp it, which doubles the reads of the one "
        f"pass that touches every track in the library, reads={reads}"
    )
    assert len(adopt_revert.read(cfg).snapshots) == 2


def test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN(
    cfg, tmp_path, monkeypatch
):
    """The headline cost, counted per file rather than asserted in a docstring.

    Round 7's ``_found_by_its_bytes`` filtered its candidates on
    ``record.size is not None``, which is a fact about the RECORD and never a
    comparison against the file in hand, and it ran the whole-file read BEFORE the
    test that empties the candidate list. So a perfectly healthy ledger, every one
    of whose records still resolves, hashed each new file twice: once to look it
    up against records that could not have matched, and once to stamp it.

    Measured on eight files at the time: ``1, 2, 2, 2, 2, 2, 2, 2`` = 15 reads for
    8 files, where 8 stamps is the floor. This asserts the per-file list rather
    than the total, so a fix that moved a read from one file to another could not
    hide in the sum.
    """
    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    monkeypatch.setattr(
        adopt_revert, "digest_of", lambda p, **kw: (reads.append(p), real_digest(p))[1]
    )

    per_file: list[int] = []
    for index in range(8):
        track = _synth_in(tmp_path / f"track{index}", ".flac")
        tags.write_genre(track, f"User Genre {index}")
        reads.clear()
        adopt_revert.write_tag_with_record(
            cfg, track, field="genre", written="Adopted Bucket", entry_id=f"e{index}"
        )
        per_file.append(len(reads))

    assert per_file == [1] * 8, (
        f"a first adoption into an empty ledger read some file more than once "
        f"per track, which is the whole-library pass paying twice: {per_file}"
    )
    assert sum(per_file) == 8
    assert len(adopt_revert.read(cfg).snapshots) == 8


def test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record(
    cfg, tmp_path
):
    """A path that will not resolve because its VOLUME is absent is not a deletion.

    THE DEFECT ROUND 7 INTRODUCED, and it is this module's oldest recurring shape
    pointed at the one function written to prevent it: absence read as evidence of
    absence. ``_found_by_its_bytes`` decided a record was STRANDED, and therefore
    available to whatever else carried its bytes, from
    ``not Path(record.path).exists()`` alone.

    Driven on a real ``hdiutil`` MS-DOS FAT image and reproduced portably here.
    The track is adopted on a detachable volume. A byte identical backup exists
    elsewhere, which is what a backup IS. The volume is detached, so the recorded
    path stops resolving. The next adoption of the BACKUP was handed the volume
    file's record: the backup's own value was overwritten with nothing recorded,
    and when the volume came back the original track was adopted afresh with
    ADOPTION'S OWN value stored as its original. One user value in no file and no
    record, on a library that lives on a drive that gets unplugged.

    The volume is simulated by removing the directory the mount point stands in,
    which is exactly what an eject leaves behind: the file's parent is not there
    to be asked.
    """
    volume = tmp_path / "Volumes" / "PORTABLE"
    on_the_volume = _synth_in(volume, ".flac")
    tags.write_genre(on_the_volume, "Volume Own Genre")

    adopt_revert.write_tag_with_record(
        cfg, on_the_volume, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.original == ("Volume Own Genre",)
    assert held.digest_state is adopt_revert.DigestState.RECORDED

    # The backup is byte for byte what adoption left, which is the whole point of
    # a backup and is exactly the evidence the byte search accepts.
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    backup = backup_dir / "probe.flac"
    backup.write_bytes(on_the_volume.read_bytes())
    assert (
        hashlib.sha256(backup.read_bytes()).hexdigest() == held.digest
    ), "the fixture did not produce a byte identical copy"

    # DETACHED. Nothing was deleted; the volume is simply not there.
    for leftover in sorted(volume.iterdir()):
        leftover.unlink()
    volume.rmdir()
    assert not Path(held.path).exists()

    adopt_revert.write_tag_with_record(
        cfg, backup, field="genre", written="Adopted Bucket", entry_id="e2"
    )
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 2, [
        (entry.path, entry.original) for entry in ledger.snapshots
    ]
    kept = [entry for entry in ledger.snapshots if entry.path == held.path]
    assert kept == [held], (
        "the copy took the record of a file whose volume was merely unplugged, "
        "so that file's own genre is now in no record at all"
    )
    # AND THE BACKUP GETS ITS OWN RECORD, recording what the BACKUP held, which
    # is adoption's value because a copy of an adopted file holds an adopted
    # file's tag. That is the honest record for it and it costs nothing: the
    # volume file's own original is still filed under the volume file.
    taken = [entry for entry in ledger.snapshots if entry.path == str(backup)]
    assert len(taken) == 1 and taken[0].original == ("Adopted Bucket",), taken

    # REPLUGGED. The record is still the volume file's, so a re-adoption finds it
    # rather than writing adoption's own value down as the original.
    volume.mkdir(parents=True)
    Path(held.path).write_bytes(backup.read_bytes())
    adopt_revert.write_tag_with_record(
        cfg, Path(held.path), field="genre", written="Adopted Bucket", entry_id="e3"
    )
    settled = [
        entry
        for entry in adopt_revert.read(cfg).snapshots
        if entry.path == held.path
    ]
    assert len(settled) == 1 and settled[0].original == ("Volume Own Genre",), (
        f"the replugged file's original is no longer recorded anywhere: {settled}"
    )


def test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped(
    cfg, tmp_path
):
    """Two agreeing addresses settle WHICH FILE, and settle nothing about content.

    Round 7 returned a match from the two agreeing addresses and never asked the
    digest, which had been diverging the whole time. Driven with no forgery: track
    A is adopted at path P; the file at P is then replaced IN PLACE by a different
    recording B, which is what ``cp`` and every truncating writer do and which
    keeps both the inode and the path. The second adoption re-stamped the record
    with B's bytes and reported clean; the revert then wrote A's genre onto B's
    audio and reported THAT clean. B's own genre was recorded nowhere, which is
    verbatim the loss ``RecordCannotBeMatched``'s own docstring says this round
    exists to prevent.

    A BYTE CHANGE IS NOT WHAT REFUSES. See the sibling below: a tag edited in
    place changes the bytes too and is accepted, because adoption's own value is
    still in the field and nothing unrecorded can be lost.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "A Own Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    first = adopt_revert.read(cfg).snapshots[0]
    assert first.original == ("A Own Genre",)
    inode = path.stat().st_ino

    other = _synth_in(tmp_path / "b", ".flac")
    tags.write_tags(other, {"title": "A Different Recording"})
    tags.write_genre(other, "B Own Genre")
    with path.open("r+b") as handle:
        handle.truncate(0)
        handle.write(other.read_bytes())
    assert path.stat().st_ino == inode, "the fixture moved the inode"
    assert tags.read_genre_from_file(path) == "B Own Genre"

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert "not the ones adoption left" in refused.value.cause.message
    assert "B Own Genre" in refused.value.cause.message
    assert "doctor" not in refused.value.cause.message

    assert tags.read_genre_from_file(path) == "B Own Genre", (
        "adoption wrote over a value it had not recorded, which is the one act "
        "this product cannot undo"
    )
    assert adopt_revert.read(cfg).snapshots == (first,), (
        "the record was re-stamped from a different recording's bytes, so the "
        "revert now accepts B and writes A's genre onto it"
    )


def test_a_TAG_EDITED_IN_PLACE_is_still_accepted_because_nothing_is_at_risk(
    cfg, tmp_path
):
    """The other half of the decision, and the reason it is not just "bytes moved".

    A mutagen save that does not go through ``os.replace`` rewrites the file in
    place: the inode stays, the path stays, and the BYTES CHANGE. That is an
    ordinary tagging session, it happens to every track somebody edits, and
    refusing it would make one tagging session cost the next adoption of the whole
    library. So a byte change on its own is not what refuses. What refuses is a
    byte change together with a value in the adopted field that neither the record
    nor this call accounts for.

    Here the tagging session edits the TITLE. The genre still holds what adoption
    wrote, so nothing unrecorded can be lost, the record keeps its original, and
    the file is never read to decide it.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    stamped = adopt_revert.read(cfg).snapshots[0]

    tags.write_tags(path, {"title": "Edited In A Tagging Session"})
    assert (
        hashlib.sha256(path.read_bytes()).hexdigest() != stamped.digest
    ), "the fixture did not change the bytes, so this proves nothing"
    assert path.stat().st_ino == Path(stamped.path).stat().st_ino

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
    )
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.file, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].written_by("e1") and ledger.snapshots[0].written_by("e2")

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "User Genre"


def test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field(
    cfg, tmp_path
):
    """The clause that reads the RECORD's ``written``, driven where it is the only one.

    Every other test in this file adopts into the same bucket twice, so the value
    the record says adoption wrote and the value this call is about to write are
    the same string and either clause alone would carry it. Here they differ: the
    first adoption wrote one bucket, a tagging session then changed the bytes, and
    the second adoption writes a DIFFERENT bucket. What is in the field is
    adoption's own value from the first run, so nothing unrecorded can be lost and
    the original is kept without the file being read to decide it.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Bucket Alpha", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.written == "Bucket Alpha"

    tags.write_tags(path, {"title": "Edited In A Tagging Session"})
    assert hashlib.sha256(path.read_bytes()).hexdigest() != held.digest

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Bucket Beta", entry_id="e2"
    )
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.written, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert tags.read_genre_from_file(path) == "Bucket Beta"


def test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write(
    cfg, tmp_path
):
    """The clause that reads THIS CALL's value, and why the record's is not enough.

    ``record.written`` is written once, by the adoption that created the record,
    and it is never updated. After a second adoption under a different taxonomy
    the file holds the SECOND bucket while the record still names the FIRST, so by
    the third adoption the record's own ``written`` no longer describes anything on
    disk. A rule that only consulted it would refuse a file whose field already
    holds exactly what is about to be written, which cannot lose anything by
    definition: a write that changes nothing destroys nothing, whatever put the
    value there.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Bucket Alpha", entry_id="e1"
    )
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Bucket Beta", entry_id="e2"
    )
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.written == "Bucket Alpha", "the record's written is not the stale one"
    assert tags.read_genre_from_file(path) == "Bucket Beta"

    tags.write_tags(path, {"title": "Edited In A Tagging Session"})
    assert hashlib.sha256(path.read_bytes()).hexdigest() != held.digest

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Bucket Beta", entry_id="e3"
    )
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.written, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].written_by("e3")


def test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH(
    cfg, tmp_path, monkeypatch
):
    """The size shortcut cannot change an answer, so only a read COUNT can see it.

    That is exactly why it needs a test of its own: a mutation that deletes it
    leaves every behavioural assertion in this file green, because the digest
    behind it reaches the same refusal one whole-file read later. The claim being
    made is about cost, so the measurement has to be about cost.

    Round 7 wrote this shortcut down in a docstring and did not have it: the
    comparison lives inside ``_look_at``, which only applies it when it is HANDED a
    recorded size, and the closure the lookup passes calls ``_look_at`` with none.
    """
    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    monkeypatch.setattr(
        adopt_revert, "digest_of", lambda p, **kw: (reads.append(p), real_digest(p))[1]
    )

    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]

    # LONGER BY CONSTRUCTION. A FLAC's padding block absorbs an ordinary tag
    # edit without the file changing length at all, which is the reason the size
    # is a shortcut and never evidence. Bytes are appended so the sizes cannot
    # agree, and the refusal below never parses this container.
    saving = tmp_path / "saving.flac"
    saving.write_bytes(path.read_bytes() + b"\x00" * 4096)
    os.replace(saving, path)
    assert path.stat().st_size != held.size, "the fixture did not move the size"

    reads.clear()
    with pytest.raises(adopt_revert.RecordCannotBeMatched):
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert reads == [], (
        f"a record whose recorded size is not this file's size was corroborated "
        f"by hashing the whole file, which no answer could depend on: {reads}"
    )


def test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger(
    cfg, tmp_path
):
    """The hardlink shape returned before the byte check, so it never reached one.

    Two names for one inode. The recorded name still resolves to this same file,
    which settles WHICH FILE and used to end the matter. It does not settle
    whether the content is still what adoption left: a hardlink is no more proof
    of that than a path is, and the file under both names can be rewritten in
    place by anything.

    So the same question is asked here as in the two-address shape, and it is
    asked in the right ORDER: this cell used to be decided by the hardlink test
    returning before the byte test was reached, which is an answer produced by
    line order rather than by evidence.
    """
    first = _synth(tmp_path, ".flac")
    tags.write_genre(first, "User Genre")
    second = tmp_path / "second-name.flac"
    os.link(first, second)

    adopt_revert.write_tag_with_record(
        cfg, first, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]

    other = _synth_in(tmp_path / "b", ".flac")
    tags.write_tags(other, {"title": "A Different Recording"})
    tags.write_genre(other, "Stranger Own Genre")
    with second.open("r+b") as handle:
        handle.truncate(0)
        handle.write(other.read_bytes())
    assert first.stat().st_ino == second.stat().st_ino, "the fixture broke the link"
    assert Path(held.path).exists(), "the recorded name must still resolve"

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        adopt_revert.write_tag_with_record(
            cfg, second, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert "Stranger Own Genre" in refused.value.cause.message
    assert adopt_revert.read(cfg).snapshots == (held,)
    assert tags.read_genre_from_file(second) == "Stranger Own Genre"


def test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut(
    cfg, tmp_path
):
    """The size can rule a record out and can never rule one in, so pin the digest.

    A refusal reached by the size comparison alone would leave the digest check
    untested on this path, and the size is the cheap fact this module says twice
    over is not evidence about content. Here the replacement is padded to exactly
    the recorded length, so the only thing left that can tell the two apart is the
    sha256.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "A Own Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]

    other = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(other, "B Own Genre")
    payload = bytearray(other.read_bytes())
    assert held.size is not None
    if len(payload) < held.size:
        payload.extend(b"\x00" * (held.size - len(payload)))
    del payload[held.size :]
    with path.open("r+b") as handle:
        handle.truncate(0)
        handle.write(bytes(payload))
    assert path.stat().st_size == held.size, "the fixture did not match the size"
    assert hashlib.sha256(path.read_bytes()).hexdigest() != held.digest

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert "not the ones adoption left" in refused.value.cause.message
    assert adopt_revert.read(cfg).snapshots == (held,)


def test_TWO_RECORDS_for_ONE_FILE_AND_FIELD_never_reach_the_lookup_at_all(
    cfg, tmp_path
):
    """The cell a hardlinked second path used to be able to write.

    A file under two names, each with its own record for the same field, is two
    answers to "what was this file's genre before adoption". Nothing downstream
    can choose between them, and the choice decides what a user's audio ends up
    holding. ``_record_for`` stops this build WRITING the second record; this is
    the other end, for a document already on disk.

    The whole document is refused at the reader with every original in it intact,
    rather than half of it being spent before the contradiction is noticed. So the
    lookup never runs and there is no shape in ``_record_for`` for this: that is
    the answer to the cell rather than a gap in it.
    """
    first = _synth(tmp_path, ".flac")
    tags.write_genre(first, "User Genre")
    second = tmp_path / "second-name.flac"
    os.link(first, second)
    adopt_revert.write_tag_with_record(
        cfg, first, field="genre", written="Adopted Bucket", entry_id="e1"
    )

    document = json.loads(adopt_revert.path_for(cfg).read_text())
    twin = dict(document["snapshots"][0])
    twin["path"] = str(second)
    twin["original"] = ["Adopted Bucket"]
    document["snapshots"].append(twin)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))

    with pytest.raises(adopt_revert.RevertLedgerUnreadable) as refused:
        adopt_revert.read(cfg)
    assert "two records for" in refused.value.cause.message

    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.write_tag_with_record(
            cfg, second, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    assert tags.read_genre_from_file(first) == "Adopted Bucket"


def test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED(
    cfg, tmp_path
):
    """Every message here ended by naming a command the build does not have.

    An instruction that cannot be carried out is worse than none, because the
    person spends the failure looking for the command instead of at the ledger.
    The machine readable remedy stays ``RUN_DOCTOR``, which is this repository's
    slug for it in five modules; the residual titled "the refusal's remedy names
    a verb that has not landed" carries that half.

    THE SUBJECT WAS ``doctor`` AND IS NOW WHATEVER IS STILL PLANNED. This test was
    written while ``crate doctor`` answered ``invalid choice: 'doctor'``, and it
    opened by asserting that, so that the day doctor landed the test would fail
    and say it had gone stale rather than quietly assert about a verb that now
    exists. That day was the U27 merge, 2026-08-15, and this is that failure being
    answered rather than deleted: the forbidden set is now DERIVED from the
    registry's own ``planned_in`` marks, so it follows every unit that lands and
    every one that does not, and the property outlives the verb it was written
    about.

    U25 landed the last two planned verbs, so the derived set is empty. The
    planned-name half is then a tautology, which this repository refuses to
    leave silent: a later planned verb re-enters the set and the original
    assertion bites again. The "Run the" half still forbids a shape in the
    messages themselves.

    Each refusal below is built through the public API rather than by calling the
    message helpers, so a new message that reintroduces the instruction is caught
    wherever it is added.
    """
    from cratekit.cli import registry as cli_registry

    planned = {one.name for one in cli_registry.entries() if one.planned_in}
    assert "doctor" not in planned, (
        "doctor is planned again, which would make the U27 merge's discharge of "
        "the cratekit.cli.doctor countdown entry wrong"
    )

    said: list[str] = []

    replaced = _synth(tmp_path, ".flac")
    tags.write_genre(replaced, "A Own Genre")
    adopt_revert.write_tag_with_record(
        cfg, replaced, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    other = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(other, "B Own Genre")
    with replaced.open("r+b") as handle:
        handle.truncate(0)
        handle.write(other.read_bytes())
    with pytest.raises(adopt_revert.RecordCannotBeMatched) as value_refusal:
        adopt_revert.write_tag_with_record(
            cfg, replaced, field="genre", written="Adopted Bucket", entry_id="e2"
        )
    said.append(value_refusal.value.cause.message)

    saved = _synth_in(tmp_path / "saved", ".flac")
    tags.write_genre(saved, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, saved, field="genre", written="Adopted Bucket", entry_id="e3"
    )
    moving = tmp_path / "moving.flac"
    moving.write_bytes(saved.read_bytes())
    tags.write_tags(moving, {"title": "Retagged Elsewhere"})
    os.replace(moving, saved)
    with pytest.raises(adopt_revert.RecordCannotBeMatched) as path_refusal:
        adopt_revert.write_tag_with_record(
            cfg, saved, field="genre", written="Adopted Bucket", entry_id="e4"
        )
    said.append(path_refusal.value.cause.message)

    assert len(said) == 2
    for message in said:
        named = sorted(verb for verb in planned if verb in message)
        assert not named, (
            f"a refusal names a verb this build does not have: {named} in "
            f"{message!r}"
        )
        assert "Run the" not in message, message


def test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file(cfg, tmp_path):
    """The re-run the whole module exists for must not need a digest.

    ``snapshot_before_write`` records and the stamp goes on after the write, so an
    interrupt between them leaves a record with no size, no time and no digest.
    The re-run has to find that record and KEEP its original, and there is no
    byte evidence to find it with. The identity and the path both claim it, they
    agree, and agreement is what a match is.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.digest_state is adopt_revert.DigestState.ABSENT

    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e2"
    )
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.file for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].written_by("e1") and ledger.snapshots[0].written_by("e2")


def test_an_identifier_from_NEITHER_scheme_is_refused_by_the_reader(cfg):
    """``file`` was accepted as any non-empty string, so nothing pinned its shape.

    A record spelling ``not-a-digest`` restored normally, and a build that
    changed the identity scheme left every old record in the document as a SECOND
    identity for the same file with nothing able to notice. Both widths are
    spelled here as literals rather than read off the module.
    """
    for identifier in ("not-a-digest", "a" * 23, "a" * 25, "dev-ino:1", ""):
        adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
        adopt_revert.path_for(cfg).write_text(
            json.dumps(_one_record_document(file=identifier))
        )
        with pytest.raises(adopt_revert.RevertLedgerUnreadable):
            adopt_revert.read(cfg)

    # And both shapes this build can legitimately have written are read.
    for identifier in ("a" * 24, "dev-ino:16777232:12345"):
        adopt_revert.path_for(cfg).write_text(
            json.dumps(_one_record_document(file=identifier))
        )
        assert adopt_revert.read(cfg).snapshots[0].file == identifier


def test_a_reverted_file_that_has_since_been_deleted_is_reported_not_silent(cfg, tmp_path):
    """And it is reported AS DELETED, which is the half the key alone cannot say.

    ``RevertReport.failed`` carries one reason per pair rather than a count
    because the ways this fails have different answers: a deleted file is not a
    defect, a replaced one is a refusal, and a container this build cannot write
    is a bug. Asserting only the key made the existence check kill zero tests,
    because a deleted file reaches the tag writer, mutagen refuses it, and the
    report says "the container refused the write" about a file that is not there.
    Same key, same pass, wrong answer, and a person acts on the reason.
    """
    path = _synth(tmp_path, ".flac")
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="New")
    path.unlink()
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == ()
    assert list(report.failed) == [(str(path), "genre")]
    assert report.failed[(str(path), "genre")] == "the file is no longer there"
    assert adopt_revert.read(cfg).snapshots != (), (
        "the record was dropped for a file that was never restored"
    )


def test_a_container_that_refuses_the_write_is_a_failure_not_a_restore(cfg, tmp_path):
    """The tag writer returns False rather than raising, so the return must be read.

    THE RECORD IS STAMPED SO THE GUARD LETS IT THROUGH, which is the whole point:
    with an unstamped record the guard refuses first, the container is never
    reached, and this test passes on a refusal that has nothing to do with the
    writer's return value. Asserted on the REASON, not just the key, for exactly
    that reason.
    """
    path = _synth(tmp_path, ".flac")
    adopt_revert.write_tag_with_record(cfg, path, field="genre", written="New")
    report = adopt_revert.revert_tags(cfg, restore=lambda *_: False)
    assert report.restored == ()
    assert list(report.failed) == [(str(path), "genre")]
    assert report.failed[(str(path), "genre")] == "the container refused the write"


#: EVERY container the writer claims, derived from the writer's own table rather
#: than listed beside it. A hand-kept copy named seven of eleven, and the four it
#: omitted were ``.aif``, ``.aifc``, ``.m4b`` and ``.mp4``: ``.aif`` is an
#: ordinary DJ container, and nothing anywhere asserted a relationship between
#: the two lists, so a container ADDED to the writer and not to this list showed
#: up as nothing at all (P3).
LEDGER_CONTAINERS = sorted(tags._DIALECT_BY_SUFFIX)

#: Every shape of "what the file held" that an exact reader has to preserve.
#: The first four are the losses the convenient reader has. The rest are the
#: transformations a plausible reader applies without anyone noticing, mapped by
#: mutating the reader until each one survived: normalizing composition form,
#: keeping only the first two values, deduplicating, and sorting. Each of these
#: round trips as itself or the ledger is lying.
LOSSY_SHAPES = [
    pytest.param(["House "], id="trailing-space"),
    pytest.param(["   "], id="whitespace-only"),
    pytest.param([""], id="empty-string"),
    pytest.param(["House", "Techno"], id="two-values"),
    pytest.param(None, id="absent"),
    pytest.param([unicodedata.normalize("NFD", "Café")], id="decomposed"),
    pytest.param(["A", "B", "C"], id="three-values"),
    pytest.param(["House", "House"], id="repeated-value"),
    pytest.param(["Techno", "House"], id="unsorted-values"),
]

#: Fields driven through the exact pair, one per dialect SHAPE rather than one
#: per name. ``genre`` is a native key in all three dialects, ``title`` is the
#: other native one, and ``energylevel`` is the freeform shape: ``TXXX`` in ID3
#: and a ``----`` atom in MP4, which carries bytes rather than text and is the
#: only branch where a reader has to decode. Both oracle tests asked only for
#: ``genre`` before, so a reader exact for one field and lossy for every other
#: passed.
LEDGER_FIELDS = ["genre", "title", "energylevel"]


@pytest.mark.parametrize("suffix", LEDGER_CONTAINERS)
@pytest.mark.parametrize("original", LOSSY_SHAPES)
def test_the_ledger_records_what_the_file_ACTUALLY_HELD(cfg, tmp_path, suffix, original):
    """The ledger is the whole safety net for a write no snapshot covers.

    It was lossy before the write was even attempted, in three ways at once, and
    every one of them is a silent edit rather than a visible failure:

    * ``.strip()`` on every value, so ``"House "`` records as ``"House"`` and
      comes back stripped;
    * ``.strip() or None`` collapsing empty and whitespace-only to None, which
      the ledger means as ABSENT, so the restore takes the clear branch and
      DELETES a field that was present. That is the exact confusion
      ``TagSnapshot``'s own docstring says the two-branch writer exists to
      prevent, arriving one layer earlier in the reader;
    * ``raw[0]`` on a list, so a second value is destroyed with no record that
      there was one. The ID3 containers survived that only by the accident of
      ``str(frame)`` joining on a null byte, which means it was invisible in
      exactly the containers an author probes first.

    Driven over every container because container-specific loss is the failure
    mode this module exists to prevent, and a proof in one of seven is not one.

    NOTHING HERE ASKS THE READER UNDER TEST WHAT THE ANSWER IS, and the first
    version of this test did exactly that. It defined its expectation as
    ``held = tags.read_tag_values(...)`` and then compared the ledger against
    ``held``, so both sides of every assertion moved together and the whole
    35-case guard was vacuous: a mutant restoring all three losses
    (``read_tag(...)`` wrapped in a one-tuple) left the entire suite green while
    ``["House "]`` came back ``["House"]`` and ``[""]`` came back DELETED. The
    parametrised literal was already in the test's hand and was thrown away.

    So the expectation is the LITERAL, and it is cross-checked against an ORACLE
    that reads the container itself without going through this module's reader at
    all. Two independent statements of the same fact, neither of them the
    function being verified.
    """
    path = _synth(tmp_path, suffix)
    if original is not None:
        assert tags.write_tag_values(path, "genre", original) is True

    expected = _expected_after_writing(original, suffix, "genre")
    assert _oracle_values(path, "genre") == expected, (
        "the fixture did not put on disk what this test believes it did, so "
        "every assertion below would be about the wrong file"
    )

    # THROUGH THE COMPOSED CALL, which is the shape ``apply_plan`` uses and the
    # only one that stamps. Taking the record half and writing separately left
    # every one of these parametrisations riding on an UNSTAMPED record, so the
    # 115 of them all traversed the guard's widest branch and none of them was
    # about it. That is how a branch accepting any file at all kept a death count
    # that looked like coverage.
    assert adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted"
    )[1] is True
    recorded = adopt_revert.read(cfg).snapshots[0]
    assert recorded.original == expected, (
        f"the ledger recorded {recorded.original!r} for a file the container "
        f"itself says holds {expected!r}"
    )
    assert recorded.digest_state is adopt_revert.DigestState.RECORDED

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}
    assert _oracle_values(path, "genre") == expected, "the restore was not exact"


#: The one shape a container genuinely cannot hold, stated rather than tolerated.
#: mutagen drops an ID3 text frame whose only value is the empty string, so the
#: field really IS absent afterwards and an exact reader has to say so. Derived
#: from the dialect rather than listed by suffix, so an ID3 container added to
#: the writer is covered without editing this.
def _drops_the_empty_string(suffix: str, field: str) -> bool:
    # Measured across every frame shape rather than assumed: a TXXX frame drops
    # an empty value exactly as a plain text frame does, so the rule is the
    # DIALECT and nothing finer. Guessing that TXXX kept it was wrong in five
    # parametrisations, which is the whole reason the oracle exists.
    assert field in tags.FIELDS
    return tags.dialect_of(suffix) is tags.Dialect.ID3


def _expected_after_writing(original, suffix: str, field: str) -> tuple[str, ...] | None:
    """What the file must hold, derived from the LITERAL rather than from a read."""
    if original is None:
        return None
    if original == [""] and _drops_the_empty_string(suffix, field):
        return None
    return tuple(original)


def _oracle_values(path: Path, field: str) -> tuple[str, ...] | None:
    """What the container holds, read WITHOUT the reader under test.

    A second implementation on purpose. It shares the FIELDS table, which is
    data, and shares no code at all with :func:`cratekit.core.tags.read_tag_values`,
    which is the thing being verified. A mutation in that function cannot move
    this answer with it, which is the whole property the first version of this
    test was missing.
    """
    import mutagen  # noqa: PLC0415

    handle = mutagen.File(path)
    if handle is None or handle.tags is None:
        return None
    key = tags.FIELDS[field].key_for(tags.dialect_of(path.suffix.lower()))
    if key not in handle.tags:
        return None
    raw = handle.tags[key]
    values = getattr(raw, "text", None)  # an ID3 frame carries its own list
    if values is None:
        values = raw if isinstance(raw, list) else [raw]
    return tuple(
        bytes(value).decode("utf-8") if isinstance(value, (bytes, bytearray)) else str(value)
        for value in values
    )


@pytest.mark.parametrize("field", LEDGER_FIELDS)
@pytest.mark.parametrize("suffix", LEDGER_CONTAINERS)
@pytest.mark.parametrize("original", LOSSY_SHAPES)
def test_the_exact_reader_agrees_with_the_container_itself(
    tmp_path, suffix, original, field
):
    """The reader against an oracle, with no ledger in the way.

    Separate from the ledger test above so a failure says WHICH of the two is
    wrong: the reader, or what the ledger did with what the reader returned.

    Driven over every field SHAPE as well as every container, because a reader
    exact for one key and lossy for the freeform ones is a reader that loses a
    field only some tracks have, in only some containers, which is the failure
    class this whole module exists around.
    """
    path = _synth(tmp_path, suffix)
    if original is not None:
        assert tags.write_tag_values(path, field, original) is True
    expected = _expected_after_writing(original, suffix, field)
    assert _oracle_values(path, field) == expected
    assert tags.read_tag_values(path, field) == expected


def test_the_container_list_is_the_writers_own(tmp_path):
    """Both lists, against each other, so neither can drift alone (P3).

    Derived rather than compared, which is stronger: the list IS the writer's
    table, so a container added there is driven by every test that uses it on the
    next run. This asserts the derivation is still real and that the containers
    genuinely exist, since a suffix nothing can encode would be a silently empty
    parametrisation.
    """
    assert set(LEDGER_CONTAINERS) == set(tags._DIALECT_BY_SUFFIX)
    assert len(LEDGER_CONTAINERS) == len(tags._DIALECT_BY_SUFFIX)
    assert {tags.dialect_of(s) for s in LEDGER_CONTAINERS} == set(tags.Dialect), (
        "a whole tag dialect has no container in the list that drives it"
    )
    for suffix in LEDGER_CONTAINERS:
        assert _synth_in(tmp_path / suffix[1:], suffix).exists()


@pytest.mark.parametrize("suffix", LEDGER_CONTAINERS)
def test_an_mp3s_legacy_id3v1_genre_survives_a_write_and_a_revert(cfg, tmp_path, suffix):
    """mutagen rewrites a PRESENT ID3v1 tag from the v2 frames on every save.

    An ID3v1 genre is one byte indexing a fixed list, so any v2 genre outside
    that list rewrites it to 255. The ledger tracks the v2 field, so the v2 value
    comes back and the v1 byte is destroyed, was never recorded, and is
    unrecoverable. That reaches any legacy library, and it needs BOTH tags
    present to bite, which is why a v1-only file round tripped fine and nothing
    noticed.

    Parametrized over every container even though only ``.mp3`` carries a raw v1
    trailer, because the guard that preserves it must be provably inert in the
    six that do not: WAV and AIFF hold their ID3 in a CHUNK mutagen may grow at
    the end of the file, and rewriting their last 128 bytes would be the exact
    corruption this module exists to prevent.
    """
    from tests.test_tags import _decoded_md5

    path = _synth(tmp_path, suffix)
    tags.write_genre(path, "Original Genre")
    before_audio = _decoded_md5(path)
    trailer_before = _id3v1_of(path)
    if suffix == ".mp3":
        trailer_before = _give_it_an_id3v1_genre(path, 31)
        assert trailer_before is not None and trailer_before[-1] == 31

    assert adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted"
    )[1] is True
    assert _id3v1_of(path) == trailer_before, "the write destroyed the legacy tag"

    adopt_revert.revert_tags(cfg)
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert _id3v1_of(path) == trailer_before, "the revert destroyed the legacy tag"
    assert _decoded_md5(path) == before_audio, (
        "preserving the legacy tag moved an audio byte, which is the corruption "
        "the whole tags module exists to prevent"
    )


def _id3v1_of(path: Path) -> bytes | None:
    """The file's raw ID3v1 trailer, or None. Read rather than parsed."""
    data = path.read_bytes()
    trailer = data[-128:]
    return trailer if len(data) >= 128 and trailer[:3] == b"TAG" else None


def _give_it_an_id3v1_genre(path: Path, index: int) -> bytes | None:
    """Add an ID3v1 trailer carrying one genre byte, the way a legacy tool would."""
    import mutagen.id3 as id3
    from mutagen.mp3 import MP3

    handle = MP3(path)
    if handle.tags is None:
        handle.add_tags()
    handle.tags["TCON"] = id3.TCON(encoding=3, text=["Original Genre"])
    handle.save(v1=2)
    raw = bytearray(path.read_bytes())
    assert raw[-128:-125] == b"TAG"
    raw[-1] = index
    path.write_bytes(bytes(raw))
    return _id3v1_of(path)


def test_a_record_with_no_original_KEY_is_refused_rather_than_read_as_absent(cfg):
    """Absence of a fact and absence AS a fact are not the same fact.

    ``get("original")`` answers None for a key that was never written and for a
    key explicitly set to null, and this ledger means the second one as "the
    field was absent, so restore it by DELETING". Reading the first as the second
    is the one branch in the reader that was not a positive recognition, and its
    consequence is a revert that clears a field nobody recorded anything about.
    """
    document = {
        "schema_version": adopt_revert.SCHEMA_VERSION,
        "snapshots": [
            {"file": "f", "field": "genre", "path": "/x/y.flac", "written": "Adopted"}
        ],
    }
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def _one_record_document(**overrides) -> dict:
    """A minimal readable ledger holding one record, plus whatever is overridden."""
    record = {
        "file": "f" * 24,
        "field": "genre",
        "path": "/x/y.flac",
        "original": ["Original"],
        "written": "Adopted",
        "recorded": "2026-08-03T00:00:00+00:00",
        "size": 4096,
        "mtime_ns": 1,
        "digest": "a" * 64,
        "digest_state": "recorded",
    }
    record.update(overrides)
    return {"schema_version": adopt_revert.SCHEMA_VERSION, "snapshots": [record]}


def _document_with_no_state(**overrides) -> dict:
    """:func:`_one_record_document` with the ``digest_state`` KEY REMOVED.

    Not ``digest_state=None``, which is what these tests used to pass and is a
    different document: a build that spelled an explicit null wrote a state it
    could not name, and the reader refuses that rather than deriving. What every
    caller here actually wants is the shape a build PREDATING the state wrote,
    which has no key at all.
    """
    document = _one_record_document(**overrides)
    del document["snapshots"][0]["digest_state"]
    return document


#: Every JSON shape Python calls false, plus the two it calls true. The digest was
#: read as ``str(entry.get("digest") or "")``, so ALL SIX falsy shapes read back as
#: "no digest recorded" and took a weaker path, while the truthy garbage was
#: stringified into a digest that could never match. Neither is a recognition.
@pytest.mark.parametrize(
    "digest",
    [
        pytest.param(0, id="zero"),
        pytest.param(False, id="false"),
        pytest.param([], id="empty-list"),
        pytest.param({}, id="empty-object"),
        pytest.param(12345, id="a-number"),
        pytest.param(["abc"], id="a-list"),
    ],
)
def test_a_digest_that_is_not_a_STRING_is_refused_rather_than_coerced(cfg, digest):
    """Truthiness is not a type check, and six shapes went through it silently.

    THE RECORD CARRIES NO ``digest_state`` KEY AT ALL, deliberately, so that this
    test is about the TYPE CHECK and nothing else. Measured with the state set to
    "recorded": removing the type check still killed only two of the six, because
    the four falsy shapes coerced to an empty string and were then caught by the
    contradiction check next door. Two guards were being credited to one test and
    four of these parametrisations were proving somebody else's work. With the
    key absent the derivation applies instead, nothing else can refuse the
    document, and every shape here stands or falls on the type check alone.

    It used to spell that as ``digest_state=None``, which is a DIFFERENT document
    and stopped being derivable: an explicit null is now refused for its own
    reason, so every parametrisation here would have passed on somebody else's
    guard again.
    """
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(_document_with_no_state(digest=digest))
    )
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def test_null_and_absent_are_both_NO_DIGEST_and_neither_is_an_acceptance(cfg):
    """The three shapes that legitimately mean "nothing was written down here".

    A null DIGEST, an empty-string digest, and a record with neither the digest
    nor the state key. They are the falsy shapes the old truthiness read got
    RIGHT by accident, and they have to keep working for the same reason the type
    check exists: an older document has to be readable, and none of the three may
    be mistaken for evidence.

    EVERY SHAPE HERE OMITS THE ``digest_state`` KEY rather than setting it to
    null. The two are different documents and this test is about the digest.

    Driven in one loop rather than as parametrisations, deliberately. Each shape
    is a document rather than a behaviour, so a per-shape test would multiply the
    collected count without adding an independent assertion.
    """
    for document in (
        _document_with_no_state(digest=None),
        _document_with_no_state(digest=""),
        {
            "schema_version": adopt_revert.SCHEMA_VERSION,
            "snapshots": [
                {
                    "file": "f" * 24,
                    "field": "genre",
                    "path": "/x/y.flac",
                    "original": ["Original"],
                    "written": "Adopted",
                    "recorded": "2026-08-03T00:00:00+00:00",
                }
            ],
        },
    ):
        adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
        adopt_revert.path_for(cfg).write_text(json.dumps(document))
        record = adopt_revert.read(cfg).snapshots[0]
        assert record.digest == ""
        assert record.digest_state is adopt_revert.DigestState.ABSENT


def test_a_digest_state_of_NULL_is_not_the_same_document_as_no_key_at_all(
    cfg, tmp_path
):
    """Absence of a fact and absence AS a fact, in the field that used to collapse them.

    ``entry.get("digest_state")`` answered None for a key that is missing and for
    a key explicitly set to null, so ``{"digest_state": null}`` silently took the
    older-document derivation. That is the exact distinction ``read`` refuses to
    collapse for ``original`` one screen down, and ``_digest`` states the opposite
    choice for its own field and says why. Only this one never decided.

    Driven both ways, because the asymmetry is the finding. ``null`` RESTORED the
    file while ``""`` raised, and a build that spelled null wrote a state it could
    not name.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())

    document["snapshots"][0]["digest_state"] = None
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    with pytest.raises(adopt_revert.RevertLedgerUnreadable) as refused:
        adopt_revert.read(cfg)
    assert "digest_state is None" in str(refused.value)

    # And the shape it used to be confused with still derives, which is the half
    # that must not be broken by fixing the other one.
    del document["snapshots"][0]["digest_state"]
    del document["snapshots"][0]["digest"]
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    assert (
        adopt_revert.read(cfg).snapshots[0].digest_state
        is adopt_revert.DigestState.ABSENT
    )


def test_a_state_that_DISOWNS_a_digest_it_is_holding_is_refused_too(cfg, tmp_path):
    """The contradiction check, in the direction that was never checked.

    ``recorded`` with no digest was refused from the day the state landed. The
    reverse, ``absent`` or ``unreadable`` on a record that CARRIES one, went
    straight through, and the guard then reported "this record carries no digest,
    so nothing in it is about the bytes at all" about a document holding a digest
    that matched the file exactly. The docstring claimed both directions.

    Driven with a digest that is the file's own, so the message is not merely
    unhelpful, it is false about what is on disk.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    assert document["snapshots"][0]["digest"] == hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    for disowning in ("absent", "unreadable"):
        document["snapshots"][0]["digest_state"] = disowning
        adopt_revert.path_for(cfg).write_text(json.dumps(document))
        with pytest.raises(adopt_revert.RevertLedgerUnreadable) as refused:
            adopt_revert.read(cfg)
        assert "carries one anyway" in str(refused.value), str(refused.value)


def test_a_document_written_BEFORE_the_state_existed_still_spends_its_digest(
    cfg, tmp_path
):
    """Back compatibility, in the direction that matters: it must still ACCEPT.

    Every ledger written before ``digest_state`` carries a digest and no state,
    and the state has to be derived from the digest rather than defaulted. A
    derivation that answered "absent" for all of them would refuse a whole
    library's undo log behind an override, which is the over-tightened direction
    and is as bad a failure as the permissive one it replaced.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    del document["snapshots"][0]["digest_state"]
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    record = adopt_revert.read(cfg).snapshots[0]
    assert record.digest and record.digest_state is adopt_revert.DigestState.RECORDED

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_record_claiming_a_digest_it_does_not_carry_is_refused(cfg):
    """A state and a digest that contradict each other cannot both be believed.

    ``digest_state`` exists so an empty digest stops meaning two things. A record
    that says "recorded" and carries nothing puts the ambiguity straight back,
    with the added problem that the record is now asserting evidence it does not
    have.
    """
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(_one_record_document(digest="", digest_state="recorded"))
    )
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def test_a_digest_state_this_build_does_not_know_is_refused(cfg):
    """Positive recognition, like every other field in this reader.

    A state nobody recognizes cannot be guessed into one of the three, because two
    of the three refuse and one accepts, and guessing wrong in that direction is
    the file nobody can put back.
    """
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(_one_record_document(digest_state="probably-fine"))
    )
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def test_a_file_replaced_since_adoption_wrote_it_is_refused_not_overwritten(cfg, tmp_path):
    """The record named a path and nothing else, so it described any bytes there.

    Record the original, let the user replace the file with a different one, and
    the revert wrote the first file's tag onto the second file's audio while
    reporting a clean restore. So the record carries what adoption LEFT, stamped
    after the write rather than before it, and a mismatch is a named refusal.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _record, landed = adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    assert landed and tags.read_genre_from_file(path) == "Adopted"

    replacement = _synth_in(tmp_path / "other", ".flac")
    tags.write_genre(replacement, "Different B")
    path.write_bytes(replacement.read_bytes())

    report = adopt_revert.revert_tags(cfg)
    assert report.restored == ()
    assert list(report.failed) == [(str(path), "genre")]
    assert tags.read_genre_from_file(path) == "Different B", (
        "the revert put one file's tag onto another file's audio"
    )
    assert adopt_revert.read(cfg).snapshots != (), (
        "the record was dropped for a file that was never restored"
    )


def test_a_later_write_of_another_field_refuses_and_says_so_per_record(cfg, tmp_path):
    """The one legitimate library this guard cannot recognize, held to explicitly.

    ``energylevel`` is in this module's own ``FIELDS`` table, put there for the
    analysis workflow, so writing one after an adoption is an ordinary thing for
    this product to do to its own library. It changes the bytes, and there is no
    evidence available without decoding the audio that separates it from somebody
    putting a different recording at the path. Two attempts to find one both let
    the catastrophic case through, so this refuses and the person overrides the
    one record.

    ASSERTED RATHER THAN LEFT UNTESTED, so the cost is visible: a reader who
    thinks this should pass silently has a test to argue with, and the residual
    titled "the adoption revert cannot recognize its own file after another
    Cratekit write"
    names what would close it properly.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    stamped = adopt_revert.read(cfg).snapshots[0]

    assert tags.write_tags(path, {"energylevel": "7"}) is True
    after = path.stat()
    assert (after.st_size, after.st_mtime_ns) != (stamped.size, stamped.mtime_ns), (
        "the fixture did not move the stamp, so this test proves nothing"
    )

    key = (str(path), "genre")
    refused = adopt_revert.revert_tags(cfg)
    assert list(refused.failed) == [key]
    assert repr(key) in refused.failed[key]
    assert adopt_revert.read(cfg).snapshots != ()

    report = adopt_revert.revert_tags(cfg, force=[key])
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert tags.read_tag(path, "energylevel") == "7", "the revert undid another field"
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_byte_identical_file_whose_time_moved_still_reverts(cfg, tmp_path):
    """A backup restore, an rsync without timestamps, a cloud re-download.

    The bytes are identical and the field still holds exactly what adoption
    wrote, which the record itself says. A guard that refused here was reading
    the circumstantial evidence and ignoring the direct evidence already in its
    hand.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    digest = hashlib.sha256(path.read_bytes()).hexdigest()

    copy = tmp_path / "restored-from-backup.flac"
    copy.write_bytes(path.read_bytes())
    path.unlink()
    copy.rename(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    os.utime(path, ns=(0, 0))

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_replacement_that_FORGES_THE_RECORDED_TIME_is_still_refused(cfg, tmp_path):
    """The modification time is metadata, and metadata is not the bytes.

    The version this replaces accepted "size and time unchanged" as its own
    definitive answer and RETURNED BEFORE the digest it had recorded was ever
    consulted. Both halves of that pair are settable by anything that copies a
    file: ``os.utime``, ``touch -r``, ``cp -p``, ``rsync -a``, ``tar -x``, and
    every tag editor carrying a preserve modification time option. So the one
    piece of evidence a replacement genuinely cannot forge sat unread in the
    record while the two it can forge decided the answer.

    Driven exactly that way. Different audio at the path, padded to the recorded
    size, stamped back to the recorded time. Measured on the previous version:
    ``restored: 1  failed: {}``, the replacement's own genre overwritten, and the
    record dropped, which is verbatim the harm the refusal message names.

    The fixture asserts the forgery worked and the digest still disagrees, so a
    green run here cannot mean the test simply failed to set the trap.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    record = adopt_revert.read(cfg).snapshots[0]
    assert record.digest and record.size is not None

    stranger = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(stranger, {"genre": "Stranger Genre", "title": "Somebody Else"})
    blob = stranger.read_bytes()
    blob = blob[: record.size].ljust(record.size, b"\x00")
    path.write_bytes(blob)
    os.utime(path, ns=(record.mtime_ns, record.mtime_ns))

    info = path.stat()
    assert (info.st_size, info.st_mtime_ns) == (record.size, record.mtime_ns), (
        "the forgery did not take, so this test proves nothing about the guard"
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() != record.digest, (
        "the fixture put the SAME bytes back, so there is nothing to refuse"
    )

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), (
        "size and time were forged and the recorded digest was never asked, so "
        "the revert put one file's tag onto another file's audio"
    )
    assert list(report.failed) == [key]
    assert tags.read_genre_from_file(path) == "Stranger Genre"
    assert adopt_revert.read(cfg).snapshots != (), "the record was dropped anyway"


def test_a_file_of_a_DIFFERENT_SIZE_is_refused_without_reading_it(cfg, tmp_path):
    """Different sizes cannot be the same bytes, so the digest is not asked.

    The one short-circuit left in front of the digest, and it is kept only
    because it can never change an answer: no digest read can rescue a size
    mismatch. Asserted as ZERO READS rather than as the refusal, because the
    refusal happens either way and the reason to keep the branch at all is that
    it does not hash a whole file to learn something ``stat`` already said.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    record = adopt_revert.read(cfg).snapshots[0]
    path.write_bytes(path.read_bytes() + b"\x00" * 4096)
    assert path.stat().st_size != record.size

    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    adopt_revert.digest_of = lambda p: (reads.append(p), real_digest(p))[1]
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        adopt_revert.digest_of = real_digest

    assert list(report.failed) == [(str(path), "genre")]
    assert reads == [], f"a whole file was hashed to confirm what stat said: {reads}"
    # THE LITERAL, not the constant the message is built from. A test comparing
    # the output against ``adopt_revert._NOT_THE_RECORDED_BYTES`` asserts X
    # equals X and passes whatever either of them says.
    assert (
        "its bytes are not the ones this record was stamped from, and nothing "
        "here can say whether another program wrote them or this tool did"
        in report.failed[(str(path), "genre")]
    )


def test_a_digest_recorded_with_no_size_is_still_compared_rather_than_refused(
    cfg, tmp_path
):
    """The size shortcut is a shortcut, so its absence must not become a verdict.

    ``size`` is consulted only because two different sizes cannot be the same
    bytes, which makes it free. A record carrying a digest and no size has to fall
    through to the digest rather than compare ``st_size`` against None, which
    refuses every such record forever on a comparison that means nothing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    document["snapshots"][0]["size"] = None
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    stripped = adopt_revert.read(cfg).snapshots[0]
    assert stripped.size is None and stripped.digest

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_file_that_cannot_be_READ_is_not_reported_as_somebody_elses_bytes(
    cfg, tmp_path
):
    """An input output error is not a verdict about the file's content.

    ``digest_of`` answers the empty string when it cannot read, and the empty
    string is not equal to any recorded digest, so the comparison alone would
    report "its bytes are not the ones adoption left there" about a file nobody
    has touched. That sends a person looking for a replacement that never
    happened, and it is the same shape as everything else this round removed: one
    value standing for two different facts.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    key = (str(path), "genre")
    with pytest.MonkeyPatch.context() as unreadable:
        unreadable.setattr(adopt_revert, "digest_of", lambda _p: "")
        report = adopt_revert.revert_tags(cfg)
    assert list(report.failed) == [key]
    assert "its bytes cannot be read here to compare" in report.failed[key], (
        report.failed[key]
    )
    assert "not the ones adoption left" not in report.failed[key]
    assert adopt_revert.read(cfg).snapshots != ()

    # And it is still spendable once the person says the file is theirs.
    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_READ_ONLY_file_and_directory_are_the_writers_problem_not_the_guards(
    cfg, tmp_path
):
    """The guard reads, so a mode that blocks WRITING must not become a refusal.

    Every acceptance now goes through a whole-file read, which puts the guard in
    front of cases it was never in front of before. A read-only file is still
    readable, so the guard must reach the same verdict it reaches for any other
    untouched file and let the container writer answer for itself; a refusal here
    would tell a person their file had been replaced because they had chmodded it.
    A read-only DIRECTORY is the same question one level up, and mutagen rewrites
    a FLAC in place rather than through a rename, so that one restores.
    """
    quiet = tmp_path / "readonly-dir"
    quiet.mkdir()
    path = _synth_in(quiet, ".flac")
    locked = _synth_in(tmp_path / "locked", ".flac")
    for target in (path, locked):
        tags.write_genre(target, "Original Genre")
        adopt_revert.write_tag_with_record(
            cfg, target, field="genre", written="Adopted", entry_id="e1"
        )

    os.chmod(locked, 0o444)
    os.chmod(quiet, 0o555)
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        os.chmod(quiet, 0o755)
        os.chmod(locked, 0o644)

    # The file in the read-only directory restored, so the read reached it.
    assert (str(path), "genre") in report.restored, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"
    # And whatever the writer said about the read-only FILE, the guard did not
    # decide it was somebody else's audio.
    refusal = report.failed.get((str(locked), "genre"), "")
    assert "cannot be recognized as the one adoption wrote to" not in refusal, refusal


def test_a_CASE_SHIFTED_path_in_the_record_still_finds_its_own_file(cfg, tmp_path):
    """The guard stats and reads ``record.path``, so the path has to still resolve.

    On a case-insensitive volume, which is the default on the platform this
    product targets, a record whose path differs from the file's name only in case
    names the same file, and the revert must restore it exactly as it would have
    under the original spelling.

    BOTH FILESYSTEMS ARE ASSERTED RATHER THAN ONE BEING SKIPPED, because the
    property that matters holds on both and a skip would hide whichever one this
    machine is not. On a case-sensitive volume the shifted name is a different
    file that is not there, which is the EXISTENCE refusal and a fact about the
    world; what neither may produce is the guard concluding that somebody replaced
    the audio, because nothing here changed a byte.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    shifted = path.with_name(path.name.upper())
    assert shifted.name != path.name, "the fixture produced no case shift at all"

    document = json.loads(adopt_revert.path_for(cfg).read_text())
    document["snapshots"][0]["path"] = str(shifted)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))

    case_insensitive = shifted.exists()
    report = adopt_revert.revert_tags(cfg)
    if case_insensitive:
        assert report.failed == {}, report.failed
        assert tags.read_genre_from_file(path) == "Original Genre"
    else:
        assert report.failed == {(str(shifted), "genre"): "the file is no longer there"}
    for refusal in report.failed.values():
        assert "cannot be recognized as the one adoption wrote to" not in refusal


def test_an_untouched_stamped_file_still_reverts_with_no_override(cfg, tmp_path):
    """The legitimate case the digest check must not cost, held to explicitly.

    Asking for the digest on every stamped record is only safe if the ordinary
    library still passes silently, so this is the pair to the forgery test above:
    a file adoption wrote and nobody has touched since reverts with no ``force``,
    no refusal, and its record settled. A guard that made this refuse would be the
    third wrong direction rather than the fix for the second.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    record = adopt_revert.read(cfg).snapshots[0]
    assert record.digest, "an unstamped record would pass this without the check"

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert report.restored == ((str(path), "genre"),)
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert adopt_revert.read(cfg).snapshots == ()


def test_an_UNSTAMPED_record_refuses_a_file_that_was_replaced(cfg, tmp_path):
    """The widest door in the guard, and an ordinary interrupt is the key to it.

    ``snapshot_before_write`` persists the record, the mutagen tag write runs, and
    only then does the stamp go on. The whole tag write sits in that window and it
    is the slowest part of the operation, so a Ctrl C lands in it: no forgery, no
    input output error, no cloud. The record left on disk carries size None,
    mtime None and no digest, and the guard used to return "unchanged" from that
    BEFORE consulting anything at all.

    Driven the way it actually bites. Months later the DJ replaces that track with
    a DIFFERENT RECORDING: different size, different content, its own genre.
    Measured on the previous version, ``restored: 1  failed: {}``, the old genre
    written onto the stranger's audio, the replacement's own genre destroyed with
    no record anywhere, and the ledger record dropped.

    THE 115 PARAMETRISATIONS THAT USED TO DIE WITH THIS BRANCH ARE NOT THIS TEST.
    They all rode one fixture that took the record half and wrote separately, so
    they traversed the branch without ever being about it, and the suite's only
    mention of "unstamped" was a precondition assert. This is the assertion that
    was missing, and it fails against the code that shipped in round 4.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    # THE INTERRUPT: the record half lands, the tag write never does.
    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    record = adopt_revert.read(cfg).snapshots[0]
    assert (record.size, record.mtime_ns, record.digest) == (None, None, "")
    assert record.digest_state is adopt_revert.DigestState.ABSENT

    # MONTHS LATER: a different recording at the same path.
    stranger = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(stranger, {"genre": "Stranger Genre", "title": "Somebody Else"})
    path.write_bytes(stranger.read_bytes())
    assert tags.read_genre_from_file(path) == "Stranger Genre", (
        "the fixture did not put a different recording at the path, so this test "
        "proves nothing about what an unstamped record accepts"
    )

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), (
        "an unstamped record accepted a file it has no evidence about at all, "
        "and the revert put one file's tag onto another file's audio"
    )
    assert list(report.failed) == [key]
    # THE LITERAL IN FULL. Asserting the leading clause left the tail
    # unpinned, so every word after "there" could be reworded and no test moved.
    assert (
        "adoption never finished recording what it left there, which is a run "
        "interrupted between the tag write and the stamp"
    ) in report.failed[key], report.failed[key]
    assert repr(key) in report.failed[key], (
        "the refusal does not name the record it can be overridden for"
    )
    assert tags.read_genre_from_file(path) == "Stranger Genre"
    assert adopt_revert.read(cfg).snapshots != (), "the record was dropped anyway"


def test_an_UNSTAMPED_record_is_still_spendable_with_force(cfg, tmp_path):
    """The other direction, which is what makes the refusal safe to add.

    A record that can never be spent is as bad as one that spends itself on the
    wrong file: the crash between the write and the stamp leaves a file genuinely
    carrying adoption's value, and the person who knows that has to be able to say
    so. That is why the refusal names the pair, and it is per record, so saying it
    about this file says nothing about any other.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    tags.write_genre(path, "Adopted")  # the write that landed before the crash
    key = (str(path), "genre")

    assert list(adopt_revert.revert_tags(cfg).failed) == [key]
    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed
    assert tags.read_genre_from_file(path) == "Original A"
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_stamping_read_that_FAILS_is_recorded_as_its_own_state(cfg, tmp_path):
    """"The digest could not be computed" and "no digest exists" are two facts.

    ``digest_of`` answered the empty string on any ``OSError`` and ``_stamped``
    stored it without comment, producing a record with size, time and no digest
    that was INDISTINGUISHABLE ON DISK from a document predating digests. The
    first is a file this build wrote seconds earlier, where the read could be
    retried or the record marked; the second is history. Collapsing them meant
    nothing could ever tell them apart again, and the metadata fallback then
    accepted round 3's forgery on the strength of it.

    Both halves are pinned: the state reaches the disk under its own name, and the
    forgery is refused under it.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    with pytest.MonkeyPatch.context() as unreadable:
        unreadable.setattr(adopt_revert, "digest_of", lambda _p: "")
        record, landed = adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1"
        )
    assert landed

    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.digest == ""
    assert record.size is not None and record.mtime_ns is not None
    stored = json.loads(adopt_revert.path_for(cfg).read_text())["snapshots"][0]
    assert stored["digest_state"] == "unreadable", (
        "the failed read is not distinguishable on disk from a record that never "
        "had a digest, so nothing can ever tell the two apart afterwards"
    )

    # THE FORGERY, under this state. Different audio, padded to the recorded size,
    # stamped back to the recorded time.
    stranger = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(stranger, {"genre": "Stranger Genre", "title": "Somebody Else"})
    path.write_bytes(stranger.read_bytes()[: record.size].ljust(record.size, b"\x00"))
    os.utime(path, ns=(record.mtime_ns, record.mtime_ns))
    info = path.stat()
    assert (info.st_size, info.st_mtime_ns) == (record.size, record.mtime_ns)

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), (
        "a record whose stamping read failed accepted a forged size and time, "
        "which is round 3's defect reached through a downgraded guard"
    )
    assert (
        "adoption could not read back what it had just written, so the bytes it "
        "left were never recorded"
    ) in report.failed[key], report.failed[key]
    assert tags.read_genre_from_file(path) == "Stranger Genre"

    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed


def test_the_stamping_read_is_RETRIED_before_the_record_gives_up(cfg, tmp_path):
    """A transient failure must not cost a record its only evidence.

    The read happens microseconds after a successful write of the same file, so
    the failures that reach it are the passing ones: a descriptor exhausted by a
    parallel pass, a brief input output error. Asking twice costs nothing and
    saves the record. Asking forever would not: a permission that is not going to
    change does not become a different answer, which is why the second failure is
    recorded as a state rather than retried again.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    attempts = {"n": 0}
    real_digest = adopt_revert.digest_of

    def fails_once(target):
        attempts["n"] += 1
        return "" if attempts["n"] == 1 else real_digest(target)

    adopt_revert.digest_of = fails_once
    try:
        record, landed = adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1"
        )
    finally:
        adopt_revert.digest_of = real_digest

    assert landed and attempts["n"] == 2, attempts
    assert record.digest_state is adopt_revert.DigestState.RECORDED
    assert record.digest == hashlib.sha256(path.read_bytes()).hexdigest()
    # And the record it saved is spendable with no override.
    assert adopt_revert.revert_tags(cfg).failed == {}
    assert tags.read_genre_from_file(path) == "Original A"


def test_a_stamping_STAT_that_fails_records_the_state_rather_than_asserting_it_cannot(
    cfg, tmp_path
):
    """The branch that carried ``pragma: no cover`` on a claim that does not follow.

    The comment read "the write above already succeeded", which says nothing about
    whether a later ``stat`` succeeds: the two are different calls against a
    filesystem that can change its mind between them. A pragma asserting a branch
    cannot happen, on a branch nothing drives, is a claim with no evidence behind
    it. It is driven here, and the record it produces refuses rather than passing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    real_stat = Path.stat
    written = {"done": False}

    def stat_fails_after_the_write(self, *args, **kwargs):
        if self == path and written["done"]:
            raise OSError(5, "the filesystem answered and then did not")
        return real_stat(self, *args, **kwargs)

    def write_then_break(target, tag_field, value):
        landed = tags.write_tags(target, {tag_field: value})
        written["done"] = True
        return landed

    with pytest.MonkeyPatch.context() as failing:
        failing.setattr(Path, "stat", stat_fails_after_the_write)
        record, landed = adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1",
            write_field=write_then_break,
        )

    assert landed
    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.size is None and record.mtime_ns is None
    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert list(report.failed) == [key]
    assert (
        "adoption could not read back what it had just written, so the bytes it "
        "left were never recorded"
    ) in report.failed[key], report.failed[key]
    assert adopt_revert.revert_tags(cfg, force=[key]).restored == (key,)


def test_a_record_with_no_digest_refuses_INSTEAD_OF_falling_back_to_the_metadata(
    cfg, tmp_path
):
    """The fallback that let round 3's forgery straight back in one layer down.

    A record carrying size and time and no digest used to be accepted on the
    metadata, on the argument that it had nothing better. It has nothing at all:
    ``os.utime`` sets the time and padding sets the size, which is exactly the
    forgery the digest was added to defeat, so the fallback re-admitted the
    catastrophic case for every record that reached it. The only test it ever had
    checked that an UNTOUCHED file passed, which any fallback does.

    So both halves are driven here, and the first is the one that was missing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    record = adopt_revert.read(cfg).snapshots[0]
    # THE OLDER DOCUMENT'S SHAPE EXACTLY: a stamp, and no digest key and no state
    # key at all, which is what a build predating the digest wrote.
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    del document["snapshots"][0]["digest"]
    del document["snapshots"][0]["digest_state"]
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    stripped = adopt_revert.read(cfg).snapshots[0]
    assert stripped.digest == ""
    assert stripped.digest_state is adopt_revert.DigestState.ABSENT
    assert stripped.size is not None and stripped.mtime_ns is not None

    # THE FORGERY, under the fallback, which nothing used to drive. Different
    # audio, padded to the recorded size, stamped back to the recorded time.
    stranger = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(stranger, {"genre": "Stranger Genre", "title": "Somebody Else"})
    blob = stranger.read_bytes()[: record.size].ljust(record.size, b"\x00")
    path.write_bytes(blob)
    os.utime(path, ns=(record.mtime_ns, record.mtime_ns))
    info = path.stat()
    assert (info.st_size, info.st_mtime_ns) == (record.size, record.mtime_ns), (
        "the forgery did not take, so this test proves nothing about the fallback"
    )

    key = (str(path), "genre")
    forged = adopt_revert.revert_tags(cfg)
    assert forged.restored == (), (
        "a record with no digest accepted a file on size and time alone, which "
        "is round 3's defect reached through the fallback rather than the guard"
    )
    assert list(forged.failed) == [key]
    assert (
        "this record carries no digest, so nothing in it is about the bytes at all"
    ) in forged.failed[key], forged.failed[key]
    assert tags.read_genre_from_file(path) == "Stranger Genre"
    assert adopt_revert.read(cfg).snapshots != (), "the record was dropped anyway"

    # AND IT IS STILL SPENDABLE, because a refusal nobody can override strands the
    # only copy of a value as surely as a wrong restore overwrites one.
    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed
    assert tags.read_genre_from_file(path) == "Original A"
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway(
    cfg, tmp_path
):
    """The shortcut that skipped the only unforgeable evidence to save nothing.

    The eviction branch skipped the digest on a dataless file, on the argument
    that reading it would fetch the whole thing from a provider. Driven with the
    REAL writer rather than a stub, the acceptance it produced calls
    ``restore_tag`` one line later, mutagen opens the file, rewrites it, and the
    genre changes: the file is materialized either way, so on the accepting path
    the skip saved nothing and cost the evidence. The previous version of this
    test passed ``restore=lambda *_: True``, so the fetch the real path performs
    never happened in it and the claim in its own docstring was never tested.

    So the branch is gone and this pins what replaced it, in both halves: an
    evicted file whose bytes nobody has touched is READ, matches, and reverts
    with no override, and the read happens because the write behind it was going
    to happen anyway. The cost that remains is the residual titled "a revert
    hashes every file it considers".

    ``st_flags`` cannot be set to ``SF_DATALESS`` from userspace, so the stat is
    what is substituted. THE LITERAL IS SPELLED HERE rather than read off
    ``adopt_scan.DATALESS_FLAG``: a test that sets the flag to the same constant
    the code compares against asserts that X equals X and passes for any value
    either of them takes.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    assert adopt_revert.read(cfg).snapshots[0].digest
    assert tags.read_genre_from_file(path) == "Adopted"

    real_stat = Path.stat

    class _Evicted:
        def __init__(self, info):
            self._info = info

        def __getattr__(self, name):
            return getattr(self._info, name)

        st_flags = 0x40000000  # SF_DATALESS, from sys/stat.h

    def evicted_stat(self, *args, **kwargs):
        info = real_stat(self, *args, **kwargs)
        return _Evicted(info) if self == path else info

    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    with pytest.MonkeyPatch.context() as evicted:
        evicted.setattr(
            adopt_revert, "digest_of", lambda p: (reads.append(p), real_digest(p))[1]
        )
        evicted.setattr(Path, "stat", evicted_stat)

        # THE REAL WRITER, which is the whole difference from the version this
        # replaces: the restore below opens the file with mutagen and rewrites it.
        report = adopt_revert.revert_tags(cfg)

    assert report.failed == {}, report.failed
    assert report.restored == ((str(path), "genre"),)
    # TWO READS, AND THE COUNT IS THE COST WRITTEN DOWN RATHER THAN ROUNDED OFF.
    # The first is the prefetch outside the lock, whose whole job is to make a
    # provider materialize the file so the second one is local; the second is the
    # guard's own read under the lock, which is the only one that decides
    # anything. An earlier build had one read, outside the lock, spent under it
    # on the strength of a four value stat tuple, and that is what let a same tick
    # in place rewrite through.
    assert reads == [path, path], (
        f"the evicted file was decided about without asking the one piece of "
        f"evidence a replacement cannot forge, reads={reads}"
    )
    assert tags.read_genre_from_file(path) == "Original Genre", (
        "the accepting path did not rewrite the file, so the argument that it "
        "was going to be materialized anyway does not hold and the branch that "
        "skipped the read was buying something after all"
    )


def _legacy_ledger(cfg_value, *records) -> None:
    """Write a ledger keyed by the PREVIOUS path-digest scheme, verbatim.

    The width is spelled as ``24`` here rather than read off the module, for the
    reason every literal in this file is: a test that derives the key the code
    derives passes for whatever width either of them takes.
    """
    snapshots = []
    for path, original, digest in records:
        snapshots.append(
            {
                "file": hashlib.sha256(
                    locations.location_to_path(str(path)).encode("utf-8")
                ).hexdigest()[:24],
                "field": "genre",
                "path": str(path),
                "original": [original],
                "written": "Adopted Bucket",
                "recorded": "2026-08-03T00:00:00+00:00",
                "size": Path(path).stat().st_size,
                "mtime_ns": Path(path).stat().st_mtime_ns,
                "digest": digest,
                "digest_state": "recorded",
            }
        )
    adopt_revert.path_for(cfg_value).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg_value).write_text(
        json.dumps(
            {"schema_version": adopt_revert.SCHEMA_VERSION, "snapshots": snapshots}
        )
    )


#: One revert pass, in a real interpreter, reporting as JSON. For the properties
#: that cannot be asserted in the process they are about: a pass that never
#: returns takes the whole suite with it rather than failing one test.
_REVERT_IN_A_CHILD = """
import json, sys
from pathlib import Path

from cratekit.adopt import revert as adopt_revert
from cratekit.core import config
from tests.test_config import valid_data

resolved = config.from_dict(valid_data(Path(sys.argv[1])))
report = adopt_revert.revert_tags(resolved)
print(json.dumps({
    "restored": [list(pair) for pair in report.restored],
    "failed": {"|".join(pair): why for pair, why in report.failed.items()},
}))
"""


def test_TWO_RECORDS_for_ONE_FILE_refuse_and_are_not_offered_a_force(cfg, tmp_path):
    """The shape that destroyed the value, driven end to end on the ledger on disk.

    :func:`identity_of` stops this build from writing two records for one file.
    It does nothing about the ledgers already written, where two spellings of one
    path each produced a record and the second one's ``original`` is the value
    adoption itself wrote. In ledger order the good record restored the real
    genre, the bogus record was then refused because the restore had changed the
    bytes, the refusal said the file's bytes were not adoption's and handed over
    a ``force`` key, and forcing wrote ``Adopted Bucket`` on as though it were the
    original. The user's genre was then in no file and no record.

    So the pass now refuses BOTH records, restores nothing, and the refusal names
    the ledger rather than the file and offers no override at all: ``force``
    overrides evidence about bytes and cannot supply which record belongs to the
    file.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Adopted Bucket")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    # Two records, one file, exactly as the two-spellings defect left it.
    _legacy_ledger(
        cfg,
        (path, "User Genre", digest),
        (str(path).replace("probe", "PROBE"), "Adopted Bucket", digest),
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    document["snapshots"][1]["path"] = str(path)
    document["snapshots"][1]["file"] = "b" * 24
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    assert len(adopt_revert.read(cfg).snapshots) == 2

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), report.restored
    assert list(report.failed) == [key]
    assert (
        "more than one record in this ledger names the file at that path, so "
        "which of their originals belongs to it cannot be decided from the ledger"
    ) in report.failed[key], report.failed[key]
    assert "force=" not in report.failed[key], (
        "the refusal still offers the override that completed the data loss"
    )
    assert tags.read_genre_from_file(path) == "Adopted Bucket"

    # AND THE OVERRIDE DOES NOT REACH IT EITHER, which is the half that matters:
    # a person who reads the old advice and types it must not be able to spend a
    # record whose original is adoption's own value.
    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (), forced.restored
    assert len(adopt_revert.read(cfg).snapshots) == 2


def test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught(
    cfg, tmp_path
):
    """The window a metadata-decided acceptance left in front of the byte-decided one.

    The pass used to read every file before taking the lock and spend that answer
    under the lock whenever ``(st_dev, st_ino, st_size, st_mtime_ns)`` had not
    moved. Those are the four values this module's own ``TagSnapshot`` docstring
    says in capitals are NOT evidence about content, deciding whether evidence
    about content still applied.

    Driven on a real FAT image, whose modification time granularity is one
    second: an in-place rewrite of the same length inside one tick left the stamp
    identical at ``(16777240, 18446744073709551613, 8430, 1785819572000000000)``
    while the actual digest moved from ``49bb5b4096d1a3f1`` to ``c1aa3237644fcf74``,
    and the restore ran on the replaced bytes. ``os.utime``, ``cp -p`` and
    ``rsync -a`` reach the same place on any filesystem, which is why this drives
    it with ``os.utime`` here rather than needing the image.

    THE SWAP HAPPENS BETWEEN THE TWO READS, which is the only placement that
    measures anything: a swap before the pass is caught by any version, and a swap
    after the restore is a different fact. The first read is the prefetch, the
    file is replaced the instant it returns, and the read that decides is the one
    taken under the lock.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    record = adopt_revert.read(cfg).snapshots[0]

    # A DIFFERENT recording of exactly the same length: same encoder, same
    # duration, a genre string of the same width. Different bytes, same size.
    other = _synth_in(tmp_path / "other", ".flac")
    tags.write_genre(other, "Adopted Buckex")
    replacement = other.read_bytes()
    assert len(replacement) == path.stat().st_size, "the fixture changed the size"
    assert replacement != path.read_bytes()

    before = path.stat()
    swapped: list[bool] = []
    real_digest = adopt_revert.digest_of

    def swap_the_bytes_after_the_first_read(target, **kwargs):
        answer = real_digest(target, **kwargs)
        if not swapped:
            swapped.append(True)
            with open(path, "r+b") as handle:  # IN PLACE, so the inode holds
                handle.write(replacement)
            os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        return answer

    with pytest.MonkeyPatch.context() as swapping:
        swapping.setattr(adopt_revert, "digest_of", swap_the_bytes_after_the_first_read)
        report = adopt_revert.revert_tags(cfg)

    after = path.stat()
    assert (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) == (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    ), "the fixture moved a stat field, so this measures the stat and not the bytes"
    assert hashlib.sha256(path.read_bytes()).hexdigest() != record.digest

    key = (str(path), "genre")
    assert report.restored == (), report.restored
    assert tags.read_genre_from_file(path) == "Adopted Buckex", (
        "the restore ran on bytes this pass had never read, which is an "
        "acceptance decided by four values that are not about content"
    )
    # AND THE REFUSAL IS PINNED IN FULL, wrapper and reason together. Three of
    # this message's clauses could be reworded with no test moving, because it
    # was asserted at its middle. Equality is the only assertion that cannot be
    # satisfied by a leading substring or by appending.
    assert report.failed[key] == (
        "this record cannot be matched to the file at that path: its bytes are "
        "not the ones this record was stamped from, and nothing here can say "
        "whether another program wrote them or this tool did. Restoring the "
        "recorded original onto bytes that are not the recorded ones writes one "
        "file's tag onto another file's audio, and nothing anywhere records what "
        "it destroyed. If you know that file is the one adoption wrote to, "
        "override this ONE record by reverting with "
        f"force={key!r}. If you do not know, leave it: the record keeps the "
        "original either way and nothing is lost by deciding later."
    ), report.failed[key]


def test_a_TARGETED_revert_cannot_DISSOLVE_the_group_refusal(cfg, tmp_path):
    """Ambiguity is a property of the DOCUMENT, so it cannot be filtered away.

    The refusal was computed over the records one pass had SELECTED rather than
    over the ledger, so naming an ``entry_id`` narrowed a group of two to a group
    of one and the group refusal evaporated. Driven through the whole public API
    on a valid ledger with no forgery: the whole-ledger revert refused both and
    offered no override, ``revert_tags(entry_id="e1")`` restored one of them and
    dropped it, and the survivor then offered a ``force`` that wrote adoption's
    own value onto the file as the original. That is verbatim the chain the group
    refusal exists to close, reached by passing a public parameter.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Adopted Bucket")
    info = path.stat()
    common = {
        "field": "genre",
        "path": str(path),
        "written": "Adopted Bucket",
        "recorded": "2026-08-03T00:00:00+00:00",
        "size": info.st_size,
        "mtime_ns": info.st_mtime_ns,
        "digest": hashlib.sha256(path.read_bytes()).hexdigest(),
        "digest_state": "recorded",
    }
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(
            {
                "schema_version": adopt_revert.SCHEMA_VERSION,
                "snapshots": [
                    {
                        **common,
                        "file": "a" * 24,
                        "original": ["User Genre"],
                        "entry": "e1",
                        "entries": ["e1"],
                    },
                    {
                        **common,
                        "file": "b" * 24,
                        "original": ["Adopted Bucket"],
                        "entry": "e2",
                        "entries": ["e2"],
                    },
                ],
            }
        )
    )
    assert len(adopt_revert.read(cfg).snapshots) == 2
    key = (str(path), "genre")

    whole = adopt_revert.revert_tags(cfg)
    assert whole.restored == (), whole.restored

    targeted = adopt_revert.revert_tags(cfg, entry_id="e1")
    assert targeted.restored == (), (
        f"naming an entry dissolved the refusal and spent a record from a group "
        f"nothing can tell apart, restored={targeted.restored}"
    )
    assert list(targeted.failed) == [key]
    assert "force=" not in targeted.failed[key]
    # THE WHOLE MESSAGE, wrapper and reason, spelled out rather than sampled. Its
    # opening clause and its closing promise that leaving it costs nothing were
    # both asserted nowhere, so either could be reworded silently.
    assert targeted.failed[key] == (
        "this record cannot be spent on the file at that path: more than one "
        "record in this ledger names the file at that path, so which of their "
        "originals belongs to it cannot be decided from the ledger. force does "
        "not apply: it overrides evidence about the BYTES, and what is missing "
        "here is which record belongs to this file, which is a fact about the "
        "ledger. The record is "
        f"{key!r}; every original is still recorded and nothing has been "
        "written."
    ), targeted.failed[key]
    # AND IT NAMES NO COMMAND, because `crate doctor` is not a verb this build
    # has: the registry marks it planned_in="U27" and the parser answers
    # `invalid choice: 'doctor'`. Every refusal in this module used to end by
    # telling the person to run it.
    assert "doctor" not in targeted.failed[key], targeted.failed[key]

    # THE OTHER SIDE OF THE GROUP, whose original is adoption's own value, is the
    # one the chain ended on. It must not be reachable by naming its entry either.
    other = adopt_revert.revert_tags(cfg, entry_id="e2")
    assert other.restored == (), other.restored

    # AND FORCE DOES NOT GET THROUGH A TARGETED PASS EITHER, which is where the
    # measured chain actually wrote the wrong value.
    forced = adopt_revert.revert_tags(cfg, entry_id="e2", force=[key])
    assert forced.restored == (), forced.restored

    assert tags.read_genre_from_file(path) == "Adopted Bucket"
    assert len(adopt_revert.read(cfg).snapshots) == 2, (
        "a record was dropped, so the original it held is now in no file and no "
        "ledger"
    )


def test_a_SINGLE_RECORD_group_is_never_refused_as_ambiguous(cfg, tmp_path):
    """The over-tightened direction, which refusing on the SCHEME would produce.

    Every ledger written before this round is keyed by a path digest, and one
    record for one file is unambiguous however it is keyed. A guard that refused
    those would strand a whole library's undo log behind a message telling the
    person to run the doctor, which is as bad a failure as the permissive one it
    replaced. So the refusal is about GROUPS and never about the scheme, and this
    drives two files whose records are keyed both ways at once.
    """
    legacy_path = _synth_in(tmp_path / "old", ".flac")
    tags.write_genre(legacy_path, "Adopted Bucket")
    _legacy_ledger(
        cfg,
        (
            legacy_path,
            "Legacy Genre",
            hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
        ),
    )
    fresh = _synth_in(tmp_path / "new", ".flac")
    tags.write_genre(fresh, "Fresh Genre")
    adopt_revert.write_tag_with_record(
        cfg, fresh, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    assert len(adopt_revert.read(cfg).snapshots) == 2

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(legacy_path) == "Legacy Genre"
    assert tags.read_genre_from_file(fresh) == "Fresh Genre"


def test_ONE_FORCE_ENTRY_overrides_EXACTLY_ONE_RECORD(cfg, tmp_path):
    """A force key reaches the record it names and never the one beside it.

    Two fields on one file are two records and one path, which is the shape
    ``_key`` exists for, so this is the ordinary case rather than a corrupt
    ledger. Driven with a restore that COUNTS, because the count is the property.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_tags(path, {"genre": "User Genre", "title": "User Title"})
    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    adopt_revert.snapshot_before_write(
        cfg, path, field="title", written="Adopted Title", entry_id="e1"
    )
    tags.write_tags(path, {"genre": "Adopted Bucket", "title": "Adopted Title"})
    assert len(adopt_revert.read(cfg).snapshots) == 2

    calls: list[tuple[Path, str]] = []

    def counting(target, tag_field, original):
        calls.append((target, tag_field))
        return adopt_revert.restore_tag(target, tag_field, original)

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg, force=[key], restore=counting)
    assert calls == [(path, "genre")], calls
    assert report.restored == (key,), report.failed
    assert set(report.restored).isdisjoint(report.failed), (
        "the same key is reported as restored and failed at once"
    )
    assert tags.read_genre_from_file(path) == "User Genre"
    assert tags.read_tag(path, "title") == "Adopted Title", (
        "the force entry reached a record it did not name"
    )


def test_a_FORCE_KEY_that_names_two_UNIDENTIFIABLE_records_overrides_neither(
    cfg, tmp_path
):
    """The residue after the ghost rule, and the one place the count guard decides.

    Where the file at the path cannot be identified at all, nothing separates two
    records carrying that path and that field, so a single ``(path, field)``
    force entry names both and can mean only one. It overrides neither and says
    which fact is missing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Adopted Bucket")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    _legacy_ledger(cfg, (path, "User Genre", digest))
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    second = dict(document["snapshots"][0])
    second["file"] = "f" * 24
    second["original"] = ["Adopted Bucket"]
    document["snapshots"].append(second)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    path.unlink()  # nothing to identify, so neither record can be told apart

    calls: list[tuple[Path, str]] = []

    def counting(target, tag_field, original):
        calls.append((target, tag_field))
        return True

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg, force=[key], restore=counting)
    assert calls == [], f"one force entry reached {len(calls)} records: {calls}"
    assert report.restored == ()
    assert (
        "more than one record in this ledger carries that path and that field, "
        "so a force key naming them cannot say which single record it means"
    ) in report.failed[key], report.failed[key]


def test_a_FIFO_at_the_recorded_path_refuses_instead_of_blocking_forever(
    cfg, tmp_path
):
    """The hang, and it held the lock that serializes every write in the library.

    ``exists`` answered True, ``stat`` answered instantly, and ``open`` never
    returned, because opening a named pipe blocks until a writer appears. The
    guard called the hash unconditionally, the hash had no bound, and the whole
    pass sits inside ``config._exclusive_lock``, so an unrelated
    ``write_tag_with_record`` on a perfectly readable file waited behind it for
    the revert's entire life. Measured: the child was still running at 6 seconds.

    The mode is now asked before a descriptor is opened, which is the same kernel
    behaviour ``adopt.scan._probe`` refuses to walk into.

    DRIVEN IN A CHILD PROCESS WITH A HARD TIMEOUT, because a hang cannot be
    asserted in the process doing the hanging: an in-process version of this test
    takes the whole suite down with it rather than failing, so the guard it is
    about cannot be mutated and measured. The child returns or it does not.

    THE RECORDED SIZE IS STRIPPED, deliberately. A FIFO reports a size of zero,
    so the size shortcut in front of the read would refuse it before any open and
    this test would pass with the mode check removed. Removing the size makes the
    read the only thing left between the pass and the open.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    document["snapshots"][0]["size"] = None
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    path.unlink()
    os.mkfifo(path)
    assert path.exists() and not path.is_file()

    environment = dict(os.environ)
    environment["PYTHONPATH"] = f"{SRC_ROOT}:{REPO_ROOT}"
    environment[config.ENV_LIBRARY_ROOT] = str(cfg.library.root)
    child = subprocess.run(
        [sys.executable, "-c", _REVERT_IN_A_CHILD, str(cfg.library.root)],
        env=environment,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert child.returncode == 0, child.stderr or child.stdout
    reported = json.loads(child.stdout)
    assert reported["restored"] == []
    assert len(reported["failed"]) == 1
    only = next(iter(reported["failed"].values()))
    assert (
        "what is at that path is not a regular file, so it has no bytes to compare"
    ) in only, only


def test_a_DIRECTORY_at_the_recorded_path_refuses_as_ITS_OWN_reason(cfg, tmp_path):
    """"that is not a file" and "its bytes cannot be read" are different facts.

    ``revert.py`` never asked ``S_ISREG``, which ``adopt.scan._probe`` does, so a
    directory at the recorded path reached the hash, the open raised
    ``IsADirectoryError``, and the person was told the bytes could not be read
    here to compare. That sends somebody looking for a permission problem.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    path.unlink()
    path.mkdir()

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert (
        "what is at that path is not a regular file, so it has no bytes to compare"
    ) in report.failed[key], report.failed[key]
    assert "cannot be read here to compare" not in report.failed[key]


def test_a_read_that_RUNS_OUT_OF_TIME_is_not_reported_as_unreadable(cfg, tmp_path):
    """``TimeoutError`` IS an ``OSError``, so a bound folded into "unreadable".

    That is the trap: a deadline raised inside ``digest_of`` was swallowed by its
    own ``except OSError`` and came back as the empty string, so a file still
    arriving from a provider was reported as a file that cannot be read, and the
    person went looking for damage that is not there. The ``except`` order in
    ``digest_of`` is what separates them, and it is asserted here through the
    refusal a person actually reads.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )

    def never_arrives(target, **_kwargs):
        raise TimeoutError(f"{target} is still being fetched")

    key = (str(path), "genre")
    real = adopt_revert.digest_of
    adopt_revert.digest_of = never_arrives
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        adopt_revert.digest_of = real

    assert report.restored == ()
    assert (
        "its bytes did not finish arriving within the time this pass waits, "
        "which is what a file still being fetched from a provider looks like"
    ) in report.failed[key], report.failed[key]
    assert "cannot be read here to compare" not in report.failed[key]


def test_the_deadline_ends_a_read_that_keeps_arriving_forever(tmp_path):
    """The bound itself, on the function that owns it.

    Asserted against a stream that never ends rather than against a slow one, so
    the test cannot pass by being faster than the deadline. The deadline is
    asked BETWEEN blocks, which is what makes it checkable at all, and the value
    passed in here is the caller's rather than the module's so the assertion is
    about the mechanism and not about the shipped patience.
    """
    endless = tmp_path / "endless.bin"
    endless.write_bytes(b"\x00" * 8)

    class _TrickleThenStop:
        """A stream that arrives too slowly, and then ENDS.

        Bounded on purpose. An unbounded one would make a build with the deadline
        removed hang the whole suite instead of failing this test, which is a
        mutation that cannot be measured. Ending after two seconds of trickle
        means the deadline is the only thing that can raise inside it.
        """

        def __init__(self):
            self.blocks = 100

        def read(self, _size):
            if not self.blocks:
                return b""
            self.blocks -= 1
            time.sleep(0.02)
            return b"\x00" * 1024

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

    original = Path.open
    stream = _TrickleThenStop()

    def trickles(self, *args, **kwargs):
        return stream if self == endless else original(self, *args, **kwargs)

    Path.open = trickles
    try:
        with pytest.raises(TimeoutError):
            adopt_revert.digest_of(endless, deadline_seconds=0.2)
    finally:
        Path.open = original
    # Counted in blocks rather than timed, R-759: the stream cannot deliver a
    # hundred blocks in under two seconds however fast the machine, and a busy
    # one slows the stream and the deadline alike, so a block count is a
    # verdict load cannot move and an elapsed time was not.
    assert stream.blocks > 0, (
        "the deadline is asked between blocks, so the read must end near it "
        "rather than run the stream out"
    )


def test_the_stamping_read_is_asked_EXACTLY_TWICE_and_not_three_times(
    cfg, tmp_path
):
    """Pinned from BOTH sides, which is what the docstring's argument requires.

    ``_STAMP_READ_ATTEMPTS`` was pinned from below only: two to one killed a
    test, two to three killed none, against a docstring arguing specifically for
    two. "A permission that is not going to change does not become a different
    answer by being asked again" is a claim about the UPPER bound and nothing
    asserted it, so the retry loop could have grown without a word changing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    attempts = {"n": 0}

    def always_fails(_target, **_kwargs):
        attempts["n"] += 1
        return ""

    real = adopt_revert.digest_of
    adopt_revert.digest_of = always_fails
    try:
        record, landed = adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1"
        )
    finally:
        adopt_revert.digest_of = real

    assert landed
    assert attempts["n"] == 2, attempts
    assert record.digest_state is adopt_revert.DigestState.UNREADABLE


def test_a_stamping_read_that_TIMES_OUT_is_not_retried_at_all(cfg, tmp_path):
    """A retry is cheap for a transient error and is the whole deadline again here.

    The argument for asking twice is that a transient failure costs nothing to
    re-ask. A read that ran out of patience costs the entire deadline a second
    time, with the ledger's lock held throughout, so the loop ends instead.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    attempts = {"n": 0}

    def times_out(target, **_kwargs):
        attempts["n"] += 1
        raise TimeoutError(f"{target} is still being fetched")

    real = adopt_revert.digest_of
    adopt_revert.digest_of = times_out
    try:
        record, landed = adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1"
        )
    finally:
        adopt_revert.digest_of = real

    assert landed and attempts["n"] == 1, attempts
    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.digest == ""


def test_a_failed_stamping_STAT_does_not_leave_a_digest_it_has_disowned(
    cfg, tmp_path
):
    """A record this build wrote could make its own ledger unreadable.

    A re-run over an already-adopted file arrives at the stamp holding the FIRST
    run's digest, and the write one line above has just rewritten the file. The
    failed-stat branch used to change only the state, producing ``unreadable``
    beside a digest describing bytes that are gone. That is exactly the
    contradiction the reader refuses in both directions, so the next ``read``
    raised on a document this build had written itself.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    assert adopt_revert.read(cfg).snapshots[0].digest

    real_stat = Path.stat
    written = {"done": False}

    def stat_fails_after_the_write(self, *args, **kwargs):
        if self == path and written["done"]:
            raise OSError(5, "the filesystem answered and then did not")
        return real_stat(self, *args, **kwargs)

    def write_then_break(target, tag_field, value):
        landed = tags.write_tags(target, {tag_field: value})
        written["done"] = True
        return landed

    Path.stat = stat_fails_after_the_write
    try:
        record, _landed = adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e2",
            write_field=write_then_break,
        )
    finally:
        Path.stat = real_stat

    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.digest == "" and record.size is None and record.mtime_ns is None
    # The document this build just wrote is readable, which is the finding.
    assert adopt_revert.read(cfg).snapshots[0].digest == ""


def test_the_FETCH_happens_before_the_lock_and_the_DECIDING_read_happens_under_it(
    cfg, tmp_path
):
    """Two reads, and which of them is allowed to decide anything.

    THIS TEST USED TO ASSERT THE OPPOSITE AND THE OPPOSITE WAS WRONG. It required
    the guard's whole-file read to happen OUTSIDE the exclusive lock, on the
    argument that a provider fetch must not block every apply and revert in the
    library. That argument is still true about the FETCH. It is false about the
    DECISION, because an answer taken before the lock has to be validated when the
    lock is finally held, and the only values available to validate it with are
    size, modification time, device and inode. This module's own TagSnapshot
    docstring says in capitals that none of those is evidence about content.
    Measured on a real FAT image, whose modification time granularity is one
    second: a file rewritten in place, same length, same tick, produced an
    identical four value tuple while its digest had changed, and the restore ran
    on the replaced bytes.

    So both reads exist and only the second one counts. The first materializes the
    file with no lock held, which is what keeps a download off the library's
    critical section. The second is the guard's, under the lock, on bytes nothing
    this pass controls has touched since.

    Asserted by asking whether the lock is takeable AT THE MOMENT OF EACH READ,
    from this same process through a second descriptor, which is exactly what a
    concurrent writer does. The expected answer is the LIST rather than a
    membership test, so neither read can be dropped without this failing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )

    held_during_read: list[bool] = []
    real = adopt_revert.digest_of

    def note_the_lock(target, **kwargs):
        handle = os.open(adopt_revert.lock_path(cfg), os.O_RDWR | os.O_CREAT)
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            held_during_read.append(False)
            fcntl.flock(handle, fcntl.LOCK_UN)
        except OSError:
            held_during_read.append(True)
        finally:
            os.close(handle)
        return real(target, **kwargs)

    adopt_revert.digest_of = note_the_lock
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        adopt_revert.digest_of = real

    assert report.failed == {}, report.failed
    assert held_during_read == [False, True], (
        "the two reads are the prefetch and the guard's own, in that order: the "
        "first must run with no lock held so a provider download does not block "
        "the library, and the second must run with the lock held so nothing can "
        "be decided on bytes read before this pass began"
    )
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_bytes_THIS_PASS_ITSELF_replaced_are_never_accepted_on(cfg, tmp_path):
    """The pass must not accept a record on bytes its own earlier restore destroyed.

    The pass reads every file before it takes the lock, so a record restored
    EARLY in the pass changes bytes an answer taken before the lock still
    describes. Accepting on that answer is a decision made from a hash of what
    the file held before this same pass rewrote it, which is the module's
    recurring defect arriving through its own optimisation.

    THE FIX IS NOT A DATED ANSWER, AND THAT VERSION SHIPPED AND WAS WRONG. An
    answer used to be stamped with ``(st_dev, st_ino, st_size, st_mtime_ns)`` and
    spent while a ``stat`` under the lock still equalled it, and a same-length
    in-place rewrite inside one modification-time tick defeats all four; see
    ``test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught``.
    Nothing taken before the lock decides anything now, so this case is covered
    by the read simply being taken again. Driven with two fields on one file, the
    second carrying the digest of the bytes the FIRST one's restore destroys.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_tags(path, {"genre": "User Genre", "title": "User Title"})
    # TITLE FIRST, GENRE SECOND, so the record visited first is the one whose
    # digest is current and whose restore therefore lands.
    adopt_revert.write_tag_with_record(
        cfg, path, field="title", written="Adopted Title", entry_id="e1"
    )
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    # The title record is given the file EXACTLY as it stands now, which is what
    # the genre record's own restore is about to replace.
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    stamp = {
        "size": path.stat().st_size,
        "mtime_ns": path.stat().st_mtime_ns,
        "digest": hashlib.sha256(path.read_bytes()).hexdigest(),
        "digest_state": "recorded",
    }
    for record in document["snapshots"]:
        if record["field"] == "title":
            record.update(stamp)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))

    report = adopt_revert.revert_tags(cfg)
    assert report.restored == ((str(path), "genre"),), report.restored
    assert (str(path), "title") in report.failed, (
        "a record was accepted on a digest of the bytes this same pass had "
        "already replaced, which is an acceptance on evidence about nothing"
    )
    assert tags.read_genre_from_file(path) == "User Genre"
    assert tags.read_tag(path, "title") == "Adopted Title"


def test_the_refusal_says_the_cause_is_UNKNOWN_and_that_leaving_it_is_safe(
    cfg, tmp_path
):
    """The message told a person their file had been replaced, and then armed them.

    Several of the ways this refusal is reached are this tool's own doing: a
    second field written to the same file, a pass that died inside its own
    restore. "the file cannot be recognized as the one adoption wrote to: its
    bytes are not the ones adoption left there" reads as a finding about the
    user, and handing over a ``force`` key in the same breath is what turned a
    confused ledger into a destroyed value.

    Three properties, spelled as literals: it names the ONE record, it says the
    cause cannot be determined from here, and it says that leaving it costs
    nothing.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    tags.write_genre(path, "Somebody Elses Edit")

    key = (str(path), "genre")
    why = adopt_revert.revert_tags(cfg).failed[key]
    assert (
        "its bytes are not the ones this record was stamped from, and nothing "
        "here can say whether another program wrote them or this tool did"
    ) in why, why
    assert f"override this ONE record by reverting with force={key!r}" in why, why
    assert (
        "If you do not know, leave it: the record keeps the original either way "
        "and nothing is lost by deciding later."
    ) in why, why


def test_the_dataless_flag_is_the_value_the_platform_header_actually_defines():
    """The constant the two eviction fixtures used to be checked against.

    Both of them set ``st_flags`` to ``adopt_scan.DATALESS_FLAG`` and then
    asserted the behaviour that constant produces, which is X equals X: the flag
    could be ``0x1`` and both tests would still pass, while every file carrying
    ``UF_NODUMP`` took the eviction branch. Round 4 made that constant safety
    critical by hoisting the check in front of every digest read, and nothing
    anywhere pinned its value.

    So the value is asserted against the LITERAL from ``sys/stat.h``, where the
    line reads ``#define SF_DATALESS 0x40000000``. A change to the constant or to
    a fixture now goes red instead of quietly agreeing with itself.
    """
    assert adopt_scan.DATALESS_FLAG == 0x40000000


def test_an_interrupted_revert_pass_can_be_retried(cfg, tmp_path):
    """A pass restores a file and dies before the ledger is rewritten.

    On retry, that record's stamp no longer matches its own SUCCESSFUL restore,
    so a stamp-only guard refused it forever: the file was correct and the ledger
    kept a record nobody could ever clear, reporting a failure on every future
    pass. The field already holding the recorded original is proof the restore
    landed, and doing it again writes the same bytes and lets the record settle.
    """
    originals = {
        _synth_in(tmp_path / "one", ".flac"): "Original One",
        _synth_in(tmp_path / "two", ".flac"): "Original Two",
    }
    for path, genre in originals.items():
        tags.write_genre(path, genre)
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
        )
    assert len(adopt_revert.read(cfg).snapshots) == 2

    class _Died(RuntimeError):
        pass

    # WHICHEVER RECORD THE PASS REACHES FIRST, because the ledger sorts by the
    # file's digest and not by the order the records were made. A fixture that
    # named one path would pass or fail on a hash.
    seen: list[Path] = []

    def restore_then_die(target, field, original):
        seen.append(target)
        if len(seen) > 1:
            raise _Died("the pass died after one file and before the ledger write")
        return adopt_revert.restore_tag(target, field, original)

    with pytest.raises(_Died):
        adopt_revert.revert_tags(cfg, restore=restore_then_die)
    assert tags.read_genre_from_file(seen[0]) == originals[seen[0]]
    # THE RECORD IT FINISHED IS ALREADY GONE, which is what makes the retry
    # possible. Batching the drops to the end of the pass left this record on
    # disk describing a file that no longer matched it, so it could never be
    # recognized again and was refused forever while every other record settled.
    remaining = adopt_revert.read(cfg).snapshots
    assert len(remaining) == 1, (
        "an interrupted pass left a record for a file it had already restored"
    )
    assert remaining[0].path != str(seen[0])

    retry = adopt_revert.revert_tags(cfg)
    assert retry.failed == {}, retry.failed
    for path, genre in originals.items():
        assert tags.read_genre_from_file(path) == genre
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_pass_that_dies_BEFORE_THE_LEDGER_WRITE_still_strands_that_one_record(
    cfg, tmp_path
):
    """The window the per-record settle NARROWED rather than closed.

    Round 3 wrote the per-record drop up as eliminating the interrupted pass
    structurally, in this module's docstring and in the residual titled "the
    adoption revert cannot recognize its own file after another Cratekit write",
    and it does not.
    It moves the window from the whole pass to one record: a run that dies between
    a restore landing and that record's drop reaching the disk leaves one record
    describing bytes its own successful restore already replaced, and every retry
    refuses exactly that record. Its sibling next door proves the narrowing is
    real; this one proves the residue is real, so nobody reads the stronger claim
    off a green suite.

    THE DAMAGE IS BOUNDED AND THAT IS WHY IT IS A RESIDUAL RATHER THAN A DEFECT.
    The refused record names itself for ``force``, and forcing it writes the same
    original onto a file that already holds it. Asserted, because "bounded" is the
    whole argument for accepting it. The residual titled "an interrupted revert
    pass still strands one record".
    """
    paths = {
        _synth_in(tmp_path / "one", ".flac"): "Original One",
        _synth_in(tmp_path / "two", ".flac"): "Original Two",
    }
    for path, genre in paths.items():
        tags.write_genre(path, genre)
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1"
        )

    class _Died(RuntimeError):
        pass

    settled = adopt_revert.write
    restored: list[Path] = []
    writes = {"n": 0}

    def note(target, tag_field, original):
        restored.append(target)
        return adopt_revert.restore_tag(target, tag_field, original)

    def die_on_the_first_settle(cfg_value, ledger):
        writes["n"] += 1
        if writes["n"] == 1:
            raise _Died("the drop never reached the disk")
        return settled(cfg_value, ledger)

    adopt_revert.write = die_on_the_first_settle
    try:
        with pytest.raises(_Died):
            adopt_revert.revert_tags(cfg, restore=note)
    finally:
        adopt_revert.write = settled

    done = restored[0]
    assert tags.read_genre_from_file(done) == paths[done], "the restore did not land"
    key = (str(done), "genre")
    assert key in {
        (record.path, record.field) for record in adopt_revert.read(cfg).snapshots
    }, "the record for the restored file was dropped, so there is no window at all"

    retry = adopt_revert.revert_tags(cfg)
    assert list(retry.failed) == [key], (
        "the window is closed rather than narrowed, so this module's docstring "
        "and the residual titled 'an interrupted revert pass still strands one "
        "record' both overstate the residue and should be corrected"
    )
    assert tags.read_genre_from_file(done) == paths[done]

    # BOUNDED: the override writes the same original onto a file already holding
    # it, so the cost of the residue is one override and never a wrong value.
    cleared = adopt_revert.revert_tags(cfg, force=[key])
    assert cleared.restored == (key,)
    assert tags.read_genre_from_file(done) == paths[done]
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_death_INSIDE_the_rewrite_is_a_different_window_and_a_weaker_bound(
    cfg, tmp_path
):
    """The interrupted-pass bound covers the window AFTER the restore, not the one inside it.

    The two are different windows and only one of them is bounded. A death between
    a restore landing and its record's drop leaves a record whose forced restore
    writes the same original onto a file that already holds it, which costs one
    override and never a wrong value. A death DURING the container rewrite is
    mutagen's write window, and no undo log can put back bytes a partial write
    destroyed, so the file may be left half rewritten and this module has no bound
    to offer for that half.

    WHAT IT DOES STILL GUARANTEE is the half it owns, and that is what is driven
    here: the drop happens only after ``restore`` RETURNS, so a death inside the
    rewrite leaves the record on disk with the recorded original still in it, the
    retry refuses because the bytes are neither the recorded ones nor anything
    else it knows, and ``force`` can still reach the original. Characterised
    rather than claimed away, in the residual titled "an interrupted revert pass
    still strands one record".
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Adopted", entry_id="e1"
    )
    key = (str(path), "genre")

    class _Died(RuntimeError):
        pass

    def half_rewrite_then_die(target, _field, _original):
        # What a killed container write leaves: bytes that are neither the
        # recorded ones nor the original.
        target.write_bytes(target.read_bytes()[: len(target.read_bytes()) // 2])
        raise _Died("the process died inside the container rewrite")

    with pytest.raises(_Died):
        adopt_revert.revert_tags(cfg, restore=half_rewrite_then_die)

    surviving = adopt_revert.read(cfg).snapshots
    assert len(surviving) == 1, "the record was dropped for a restore that never landed"
    assert surviving[0].original == ("Original A",), (
        "the only copy of the original went with the interrupted rewrite"
    )
    retry = adopt_revert.revert_tags(cfg)
    assert list(retry.failed) == [key]
    assert (
        "its bytes are not the ones this record was stamped from, and nothing "
        "here can say whether another program wrote them or this tool did"
    ) in retry.failed[key], retry.failed[key]


@pytest.mark.parametrize(
    "stranger_genre",
    [
        # THE FIRST ONE IS THE CASE THE GUARD IS ACTUALLY FOR, and the round 2
        # version of this test used only the second. ``written`` is a taxonomy
        # bucket's DISPLAY name, so the value adoption writes is shared by most of
        # the library: a stranger's recording whose own genre is that bucket is
        # the LIKELIEST replacement, not an exotic one. Picking an unrelated
        # string dodged the branch under test and made the widening invisible.
        "THE BUCKET ADOPTION WROTE",
        "Different B",
    ],
    ids=["stranger-shares-the-bucket", "stranger-has-its-own-genre"],
)
def test_a_genuinely_replaced_file_is_still_refused_and_force_gets_through(
    cfg, declared, tmp_path, stranger_genre
):
    """The guard still bites, and it is evidence rather than permission (P7).

    Loosening a refusal is only safe if the case it exists for still refuses, so
    this drives the original finding again, in BOTH shapes the replacement can
    take. Measured on the version that trusted the field's value: the stranger
    variant came back ``restored: 1  failed: {}``, the replacement's own genre was
    overwritten with a record belonging to different audio, and the ledger record
    was dropped, which is verbatim the harm the refusal message names.
    """
    routable, _genre = _bucket_and_genre(declared)
    written = declared.bucket(routable).display
    if stranger_genre == "THE BUCKET ADOPTION WROTE":
        stranger_genre = written

    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written=written, entry_id="e1"
    )
    # A DIFFERENT RECORDING at the same path. Different bytes, so this is not the
    # backup-restore case; the size differs too, which is the ordinary shape.
    replacement = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(replacement, {"genre": stranger_genre, "title": "Somebody Else"})
    path.write_bytes(replacement.read_bytes())

    key = (str(path), "genre")
    refused = adopt_revert.revert_tags(cfg)
    assert refused.restored == (), (
        "the revert put one file's tag onto another file's audio"
    )
    assert list(refused.failed) == [key]
    assert repr(key) in refused.failed[key], (
        "the refusal does not name the record it can be overridden for, so a "
        "person who knows this one file is theirs cannot act on it without "
        "acting on every other refused file too"
    )
    assert tags.read_genre_from_file(path) == stranger_genre
    assert adopt_revert.read(cfg).snapshots != (), "the record was dropped anyway"

    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,)
    assert tags.read_genre_from_file(path) == "Original A"
    assert adopt_revert.read(cfg).snapshots == ()


def test_force_overrides_the_record_it_names_and_no_other(cfg, tmp_path):
    """A per-record message must not hand out a pass-wide override.

    The refusal is emitted once per record, so a person reads "override this"
    beside the one file they recognize. A boolean turns that into consent for
    every other refused record in the ledger, and those are precisely the
    dangerous ones: the benign cases already passed the guard silently.
    ``entry_id`` cannot separate them either, because two files written through
    one plan entry are two records under one identifier.
    """
    mine = _synth_in(tmp_path / "mine", ".flac")
    stranger = _synth_in(tmp_path / "stranger", ".flac")
    for path, genre in ((mine, "Original Mine"), (stranger, "Original Stranger")):
        tags.write_genre(path, genre)
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="one_entry"
        )
    for path in (mine, stranger):
        other = _synth_in(tmp_path / f"swap{path.parent.name}", ".flac")
        tags.write_tags(other, {"genre": "Replaced", "title": "Somebody Else"})
        path.write_bytes(other.read_bytes())

    assert len(adopt_revert.revert_tags(cfg).failed) == 2

    report = adopt_revert.revert_tags(cfg, force=[(str(mine), "genre")])
    assert report.restored == ((str(mine), "genre"),)
    assert list(report.failed) == [(str(stranger), "genre")]
    assert tags.read_genre_from_file(mine) == "Original Mine"
    assert tags.read_genre_from_file(stranger) == "Replaced", (
        "forcing one record overwrote a file the person never named"
    )

    # Nor can the entry identifier stand in for naming them, since both records
    # were written through one plan entry.
    both = adopt_revert.revert_tags(cfg, entry_id="one_entry")
    assert list(both.failed) == [(str(stranger), "genre")]


def test_one_unreadable_record_costs_one_record_not_the_pass(cfg, tmp_path):
    """The per-track rule U19 paid for, applied to the undo log.

    ``record.field`` comes off disk, where ``read`` recognizes it as a non-empty
    string and deliberately does NOT check it against ``tags.FIELDS``: refusing a
    whole document over one unknown field would strand every other record in it.
    So a ledger written by a build with one more field is ordinary, and it used to
    raise ``ValueError`` out of the pass before the lock released, so nothing
    settled and every retry died on the same record.
    """
    good = [_synth_in(tmp_path / f"g{i}", ".flac") for i in range(2)]
    for index, path in enumerate(good):
        tags.write_genre(path, f"Original {index}")
        adopt_revert.write_tag_with_record(
            cfg, path, field="genre", written="Adopted", entry_id="e1"
        )

    # A THIRD FILE, so the bad record's own guard is satisfied and the pass truly
    # reaches the writer with an unknown field. Two things would otherwise leave
    # this test green while proving nothing about a ``ValueError`` escaping the
    # loop: an unstamped record is refused before ``tags`` is ever called, and a
    # record naming a file another record has already restored is refused because
    # that restore moved the bytes.
    odd = _synth_in(tmp_path / "odd", ".flac")
    info = odd.stat()
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    document["snapshots"].append(
        {
            "file": "a" * 24,
            "field": "bpm",  # a field THIS build does not know
            "path": str(odd),
            "original": ["124"],
            "written": "125",
            "recorded": "2026-08-03T00:00:00+00:00",
            "entry": "e1",
            "entries": ["e1"],
            "size": info.st_size,
            "mtime_ns": info.st_mtime_ns,
            "digest": hashlib.sha256(odd.read_bytes()).hexdigest(),
            "digest_state": "recorded",
        }
    )
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    assert len(adopt_revert.read(cfg).snapshots) == 3

    report = adopt_revert.revert_tags(cfg)
    assert len(report.restored) == 2, (
        "one record naming a field this build cannot write ended the pass, so "
        "nothing settled and every retry dies on the same record"
    )
    assert list(report.failed) == [(str(odd), "bpm")]
    for index, path in enumerate(good):
        assert tags.read_genre_from_file(path) == f"Original {index}"
    assert len(adopt_revert.read(cfg).snapshots) == 1, (
        "the two records that were spent are still in the ledger"
    )


def test_the_value_adoption_WROTE_is_never_treated_as_the_files_identity(
    cfg, declared, tmp_path
):
    """A bucket display name is shared by most of the library it was written to.

    This is the assertion that stops the guard being widened back into the shape
    that failed: whatever else it consults, it must not conclude "this is the file
    adoption wrote to" from the field holding a value thousands of files hold.
    Asserted about the RECORD's stored evidence rather than about a message, so
    it stays true however the checks are reordered.
    """
    routable, _genre = _bucket_and_genre(declared)
    written = declared.bucket(routable).display
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    record, landed = adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written=written, entry_id="e1"
    )
    assert landed
    info = path.stat()
    assert record.digest == hashlib.sha256(path.read_bytes()).hexdigest(), (
        "the record does not carry the bytes adoption left, so the only thing "
        "left to recognize the file by is a value the whole bucket shares"
    )
    assert (record.size, record.mtime_ns) == (info.st_size, info.st_mtime_ns)
    assert record.written == written
    assert tags.read_genre_from_file(path) == written
    # AND THE INODE IS NOT RECORDED, deliberately. It is the other thing that
    # looks like identity: the same inode is the same file and says nothing
    # about its content, because write_bytes and cp both truncate in place and
    # keep it, which is how a track is actually replaced.
    stored = json.loads(adopt_revert.path_for(cfg).read_text())["snapshots"][0]
    assert "ino" not in stored and "dev" not in stored


def test_a_targeted_revert_answers_for_the_entry_that_actually_wrote(cfg, tmp_path):
    """First-write-wins means the SECOND adoption writes through the FIRST record.

    So a targeted revert matching on the record's creator answers "nothing to do"
    for work that demonstrably happened, and returns a clean empty report while
    the file still holds the value that entry wrote.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="First", entry_id="ap_one"
    )
    adopt_revert.write_tag_with_record(
        cfg, path, field="genre", written="Second", entry_id="ap_two"
    )
    assert tags.read_genre_from_file(path) == "Second"
    records = adopt_revert.read(cfg).snapshots
    assert len(records) == 1
    assert records[0].entry_id == "ap_one", "the second write replaced the original"
    assert records[0].original == ("Original Genre",)

    report = adopt_revert.revert_tags(cfg, entry_id="ap_two")
    assert report.restored == ((str(path), "genre"),), (
        "the revert reported success for work it did not do, and the file still "
        "holds what the second adoption wrote"
    )
    assert tags.read_genre_from_file(path) == "Original Genre"

    nothing = adopt_revert.revert_tags(cfg, entry_id="ap_never_wrote_anything")
    assert nothing.restored == () and nothing.failed == {}


def test_two_failed_fields_on_one_file_are_two_reasons(cfg, tmp_path):
    """The report was keyed on the path, so one file could only carry one reason.

    The ledger stayed right through that, because it keys on the file AND the
    field. Only the half a person reads was lossy, which is the half nothing
    checks.

    BOTH RECORDS ARE OVERRIDDEN BY NAME so that the reasons being compared are
    the writer's, not the guard's. Two fields on one file is the second
    instance and the guard refuses one of them on every pass, which would give
    this test two failures and no restore whatever the report keyed on.
    """
    path = _synth(tmp_path, ".flac")
    tags.write_tags(path, {"genre": "Original Genre", "title": "Original Title"})
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="New Genre")
    adopt_revert.snapshot_before_write(cfg, path, field="title", written="New Title")

    def refuse_genre(_path, tag_field, _original):
        if tag_field == "genre":
            raise OSError("the genre frame would not write")
        return True

    report = adopt_revert.revert_tags(
        cfg, force=[(str(path), "genre"), (str(path), "title")], restore=refuse_genre
    )
    assert set(report.failed) == {(str(path), "genre")}
    assert report.restored == ((str(path), "title"),)
    assert report.files() == (str(path),)


@pytest.mark.parametrize("suffix", LEDGER_CONTAINERS)
def test_the_clear_path_removes_a_field_without_touching_the_audio(tmp_path, suffix):
    """``clear_tags`` is the undo ``write_tags`` cannot express. Same classification.

    PARAMETRIZED OVER EVERY CONTAINER, like its sibling next door. It was driven
    against ``.flac`` alone, which exercises the Vorbis branch and leaves the MP4
    branch and the ID3 branch untested, and the ID3 branch is what ``.wav`` and
    ``.aiff`` take: the two containers whose corruption this whole module exists
    to prevent. The branches turned out to work, so this closes a coverage gap
    rather than a defect, and the one operation with no snapshot behind it should
    not be the one tested in a seventh of the places its sibling is.
    """
    from tests.test_tags import _decoded_md5, _payload_chunk_digest

    path = _synth(tmp_path, suffix)
    tags.write_tags(path, {"genre": "Original Genre", "title": "Kept Title"})
    before = _decoded_md5(path)
    before_payload = _payload_chunk_digest(path)

    assert tags.clear_tags(path, ["genre"]) is True
    assert tags.read_tag(path, "genre") is None
    assert tags.read_tag(path, "title") == "Kept Title"
    assert _decoded_md5(path) == before
    assert _payload_chunk_digest(path) == before_payload
    # Clearing a field that is already gone is the state the file is already in.
    assert tags.clear_tags(path, ["genre"]) is True
    assert tags.read_tag(path, "title") == "Kept Title"


def test_clearing_an_unknown_field_raises_rather_than_deleting_something(tmp_path):
    """The beat-grid rule's enforcement point, on the deletion path too."""
    path = _synth(tmp_path, ".flac")
    with pytest.raises(ValueError):
        tags.clear_tags(path, ["bpm"])


# ═══════════════════════════════════════════════════════════════════════════
# The two readers: a wrong document is never an empty one
# ═══════════════════════════════════════════════════════════════════════════


WRONG_DOCUMENTS = [
    "[]",
    '"a string"',
    "42",
    "null",
    '{"schema_version": 1}',
    '{"schema_version": "1", "applied": []}',
    '{"applied": []}',
    '{"schema_version": 99, "applied": []}',
    '{"schema_version": 1, "applied": {}}',
    '{"schema_version": 1, "applied": [null]}',
    '{"schema_version": 1, "applied": [{"tree": "t", "content": "c", "actor": "a"}]}',
    '{"schema_version": 1, "applied": [{"entry": "e", "tree": "t", "content": "c"}]}',
]


@pytest.mark.parametrize("document", WRONG_DOCUMENTS, ids=range(len(WRONG_DOCUMENTS)))
def test_a_wrong_applied_ledger_refuses_rather_than_reading_as_empty(cfg, document):
    """An empty ledger re-applies an approved plan from its first entry.

    Every branch is a positive recognition of a field. Catching only a parse
    error leaves a top-level list, a scalar, a null records field and a document
    from another build all reading as empty, which is the shape U11 shipped and
    which then destroyed the file on the next write.
    """
    path = adopt_apply.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document)
    with pytest.raises(CratekitError) as excinfo:
        adopt_apply.read(cfg)
    assert excinfo.value.cause.reason == "adoption-ledger-unusable"
    assert path.read_text() == document, "the reader modified the document it refused"


def test_two_records_for_one_entry_refuse(cfg):
    path = adopt_apply.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"entry": "e1", "tree": "t", "content": "c", "actor": "a"}
    path.write_text(json.dumps({"schema_version": 1, "applied": [record, record]}))
    with pytest.raises(CratekitError):
        adopt_apply.read(cfg)


WRONG_REVERT_DOCUMENTS = [
    "[]",
    '"a string"',
    "null",
    '{"schema_version": 1}',
    '{"snapshots": []}',
    '{"schema_version": 99, "snapshots": []}',
    '{"schema_version": 1, "snapshots": {}}',
    '{"schema_version": 1, "snapshots": [3]}',
    '{"schema_version": 1, "snapshots": [{"file": "f", "field": "genre"}]}',
    '{"schema_version": 1, "snapshots": [{"file": "f", "field": "genre", '
    '"path": "/x", "written": "w", "original": 7}]}',
]


@pytest.mark.parametrize(
    "document", WRONG_REVERT_DOCUMENTS, ids=range(len(WRONG_REVERT_DOCUMENTS))
)
def test_a_wrong_revert_ledger_refuses_rather_than_reading_as_empty(cfg, document):
    """An empty revert ledger says nothing can be undone about writes on disk."""
    path = adopt_revert.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document)
    with pytest.raises(CratekitError) as excinfo:
        adopt_revert.read(cfg)
    assert excinfo.value.cause.reason == "adoption-ledger-unusable"


def test_a_null_original_is_a_legitimate_record(cfg):
    """None means the field was ABSENT, which the reader must not refuse."""
    path = adopt_revert.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "snapshots": [
                    {
                        "file": "f" * 24,
                        "field": "genre",
                        "path": "/x/y.flac",
                        "written": "w",
                        "original": None,
                        "recorded": "2026-08-02T00:00:00+00:00",
                    }
                ],
            }
        )
    )
    assert adopt_revert.read(cfg).snapshots[0].original is None


def test_with_snapshot_KEEPS_the_record_already_there(cfg, tmp_path):
    """The property the module docstring calls load bearing, asserted directly.

    Nothing drove it. Every path into `_record_locked` looks the record up first
    and only calls `with_snapshot` when there is none, so the branch that keeps
    the first record is unreachable from this module's own callers and survived
    being deleted. It is the last line of defence for the one thing this ledger
    exists to hold: the SECOND call happens on a re-run after a crash, by which
    time the file already carries what adoption wrote, so replacing would record
    the replacement as the original.
    """
    first = adopt_revert.TagSnapshot(
        file="dev-ino:1:2",
        field="genre",
        path="/x/y.flac",
        original=("User Genre",),
        written="Adopted Bucket",
        recorded="2026-08-03T00:00:00+00:00",
    )
    second = replace(first, original=("Adopted Bucket",))
    kept = adopt_revert.EMPTY.with_snapshot(first).with_snapshot(second)
    assert len(kept.snapshots) == 1
    assert kept.snapshots[0].original == ("User Genre",), (
        "the second record replaced the first, so the value adoption wrote is "
        "now recorded as the value it replaced"
    )
    # And the one way a record IS legitimately amended still replaces it, which
    # is what keeps this from being fixable by refusing both.
    amended = kept.replacing(second)
    assert amended.snapshots[0].original == ("Adopted Bucket",)


def test_an_original_key_that_is_ABSENT_is_refused_rather_than_read_as_null(cfg):
    """Absence of a fact and absence AS a fact, in the field that owns the phrase.

    ``entry.get("original")`` answers None for a record that says the field was
    absent and for a record that never said anything about it, and reading the
    second as the first reverts by DELETING a field this ledger never saw. The
    reader says so at length and nothing drove it: the check survived being
    deleted, because the only test in this area supplied the key.
    """
    document = _one_record_document()
    del document["snapshots"][0]["original"]
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    with pytest.raises(adopt_revert.RevertLedgerUnreadable) as refused:
        adopt_revert.read(cfg)
    assert "with no original key at all" in str(refused.value), str(refused.value)


def test_the_refusal_slug_is_declared_with_an_exit_code():
    """S4: a refusal with no reserved code collapses to a bare status."""
    assert "adoption-ledger-unusable" in REASONS
    assert REASONS["adoption-ledger-unusable"] is ExitCode.PRECONDITION


# ═══════════════════════════════════════════════════════════════════════════
# The lock, proved by real processes
# ═══════════════════════════════════════════════════════════════════════════


_CONCURRENT_MARKS = """
import sys
from pathlib import Path

from cratekit.adopt import apply as adopt_apply
from cratekit.core import config

library = Path(sys.argv[1])
worker = int(sys.argv[2])
per_worker = int(sys.argv[3])

cfg = config.from_dict(
    {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library),
            "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(library.parent / "staging")},
        "profile": {"name": "slim"},
    }
)
for index in range(per_worker):
    adopt_apply.mark_applied(
        cfg,
        adopt_apply.AppliedEntry(
            entry_id=f"ap_{worker:02d}_{index:03d}",
            tree="t",
            content_id=f"c{index}",
            bucket="b",
            sub="s",
            actor="tester",
            digest="d",
            applied="2026-08-02T00:00:00+00:00",
        ),
    )
"""


def test_concurrent_marks_from_real_processes_all_survive(cfg, library):
    """The shape this repository has shipped twice, refused a third time.

    An atomic rename makes the RENAME atomic and does nothing for the read then
    write around it. Eight real processes recording twenty-five decisions each
    left seventy-one of two hundred on the disk in the decision stores, and every
    losing call returned a record reporting success. Threads cannot see this:
    only separate processes show what actually reached the file.
    """
    workers, per_worker = 6, 20
    _in_separate_processes(
        _CONCURRENT_MARKS,
        workers=workers,
        arguments=lambda worker: (library, worker, per_worker),
    )
    landed = adopt_apply.read(cfg).entry_ids()
    assert len(landed) == workers * per_worker, (
        f"{workers * per_worker - len(landed)} records were lost to an unlocked "
        f"read-modify-write, and every losing call reported success"
    )


_APPLY_AGAINST_REVERT = """
import sys, time
from pathlib import Path

from cratekit.adopt import revert as adopt_revert
from cratekit.core import config, tags

library, role, target = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
cfg = config.from_dict(
    {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library),
            "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(library.parent / "staging")},
        "profile": {"name": "slim"},
    }
)

if role == "apply":
    def slow(path, field, value):
        # The window the revert used to fit inside, made wide enough to hit.
        time.sleep(1.0)
        return tags.write_tags(path, {field: value})

    adopt_revert.write_tag_with_record(
        cfg, target, field="genre", written="Adopted Genre",
        entry_id="ap_one", write_field=slow,
    )
else:
    time.sleep(0.3)
    adopt_revert.revert_tags(cfg)
"""


def test_a_revert_cannot_land_inside_an_apply_and_lose_the_original(cfg, library, tmp_path):
    """The window that was one instruction wide and cost the only copy.

    The ledger's lock covered each document's read-modify-write and covered
    NOTHING about an apply against a revert. Reproduced through the public entry
    points in sequence: record ``Original``, revert (which restores the file and
    empties the ledger), apply's write lands ``Adopted``, and a final revert
    returns ``restored=() failed={}``. The original is permanently gone, no
    snapshot holds it, and both reports read clean.

    Two real processes rather than two calls, because what is being proved is
    what reached the disk while another process held the lock. Note this is the
    opposite question from apply-against-apply, which was already safe: that one
    is about two writers of one record, this one is about a writer and a reader
    of the same record in opposite directions.
    """
    target = tmp_path / "track.flac"
    target.write_bytes(_synth_in(tmp_path / "source", ".flac").read_bytes())
    tags.write_genre(target, "Original Genre")

    roles = ("apply", "revert")
    _in_separate_processes(
        _APPLY_AGAINST_REVERT,
        workers=2,
        arguments=lambda worker: (library, roles[worker], target),
    )

    assert tags.read_genre_from_file(target) == "Original Genre", (
        "the apply wrote its value with no record behind it, so the original is "
        "gone and nothing in either report says so"
    )
    remaining = adopt_revert.read(cfg).snapshots
    assert all(record.original == ("Original Genre",) for record in remaining), (
        "a surviving record no longer describes the value the file started with"
    )


def test_the_apply_loop_records_and_writes_through_the_ONE_locked_call():
    """The proof above is about the composed call; this is what carries it to apply.

    Two adjacent calls, a record and then a write, have the window between them
    whatever each one locks on its own. So the source is checked rather than
    trusted: the apply loop must reach ``write_tag_with_record`` and must not
    reach ``snapshot_before_write``, which is the record HALF and is public
    because a caller may legitimately want only that.

    Bound through the import graph rather than matched by bare name, which is the
    lesson U11 paid for: three countdown guards matched attribute names with no
    binding to the module they were about, so a file that never touched the
    review queue satisfied all three.
    """
    source = (ADOPT_ROOT / "apply.py").read_text()
    tree = ast.parse(source)
    aliases = {"revert"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "cratekit.adopt":
            for alias in node.names:
                if alias.name == "revert":
                    aliases.add(alias.asname or alias.name)

    reached: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = node.func.value
            if isinstance(owner, ast.Name) and owner.id in aliases:
                reached.add(node.func.attr)

    assert "write_tag_with_record" in reached, (
        "the apply loop composes the record and the write itself, so a revert "
        "landing between them leaves the write with no original behind it"
    )
    assert "snapshot_before_write" not in reached, (
        "the apply loop takes the record half on its own, which is the window "
        "the composed call exists to close"
    )


def test_both_documents_and_their_lock_are_declared_state_entries():
    """A path composed under a state root is a file nothing walks or backs up."""
    for key in ("adoption_ledger", "adoption_tag_revert_log", "adoption_locks"):
        assert config.state_file(key) is not None


def test_the_applied_ledger_rolls_back_with_the_database(cfg):
    """COUPLED: every record it holds names a membership row a restore removes.

    A ledger that survived a rollback would report those entries applied while
    the rows were gone, and the resume would skip exactly the work the restore
    undid.
    """
    assert config.state_file("adoption_ledger").snapshot is config.SnapshotRole.COUPLED
    assert adopt_apply.path_for(cfg).parent == config.library_coupled_dir(cfg)


def test_the_revert_ledger_and_the_locks_never_roll_back(cfg):
    """The undo log argument, and the inode argument, one assertion each."""
    assert (
        config.state_file("adoption_tag_revert_log").snapshot
        is config.SnapshotRole.NEVER_RESTORED
    )
    assert config.state_file("adoption_locks").snapshot is config.SnapshotRole.NEVER_RESTORED
    assert adopt_revert.lock_path(cfg).parent == config.state_path("adoption_locks", cfg)
    assert config.library_coupled_dir(cfg) not in adopt_revert.lock_path(cfg).parents


# ═══════════════════════════════════════════════════════════════════════════
# R19, and the structured output
# ═══════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════
# The registry: a marker that can expire, and an obligation somebody owns
# ═══════════════════════════════════════════════════════════════════════════


def test_the_planned_marker_on_the_apply_verb_CAN_ACTUALLY_FIRE():
    """The countdown could never fire, in this build or in any future one.

    Both adoption verbs named ``cratekit.adoption.cli``, a package no unit's file
    list has ever declared, while every other authority says ``adopt``. The
    marker test probes with ``find_spec`` inside ``except ModuleNotFoundError``,
    and ``find_spec`` RAISES that exception on a missing PARENT rather than
    returning None, so the probe caught it and read "the parent package does not
    exist" as "the module has not landed yet". A typo in a string therefore
    disarmed a guard permanently, and closing the issue would have left two verbs
    shipping with no conformance coverage and nothing anywhere saying so.

    BOTH VERBS HAVE NOW LANDED, and this guard was rewritten rather than deleted
    when the second one did. What it asserted was never "the marker is still
    there"; it was that the PROBE ANSWERS, which is a property of the module
    strings and holds whether a verb has landed or not. Deleting it on the day it
    went green would have taken the only check on that property with it, and the
    typo it caught is a typo somebody can make again in either direction.
    """
    import importlib.util  # noqa: PLC0415

    from cratekit.cli import registry  # noqa: PLC0415

    scan_entry = registry.entry("adopt.scan")
    apply_entry = registry.entry("adopt.apply")
    assert scan_entry.module.startswith("cratekit.adopt.")
    assert apply_entry.module.startswith("cratekit.adopt.")
    assert scan_entry.module != apply_entry.module, (
        "one module string for two verbs means the marker test keys on a name "
        "they share, so the half that is ready is held back by the half that is "
        "not, and neither countdown is about itself"
    )

    # THE WHOLE DEFECT IN ONE LINE, and it is the same line either way: this call
    # used to RAISE, and the raise was caught and read as absence. Asserting the
    # spec is not None now says the module is genuinely importable AND that the
    # probe answered; before it landed, the same call had to return None rather
    # than raise. The failure the guard exists for is the raise, not the value.
    assert importlib.util.find_spec(apply_entry.module) is not None
    assert importlib.util.find_spec(scan_entry.module) is not None

    # DERIVED FROM THE REGISTRY rather than asserted as a state, so this outlives
    # both verbs: a marker and a landed module cannot both be true, in either
    # direction, for either verb.
    for entry in (scan_entry, apply_entry):
        assert entry.landed is (entry.planned_in is None), (
            f"{entry.name} says landed={entry.landed} and planned_in="
            f"{entry.planned_in!r}, so the marker and the module disagree and "
            f"the conformance suite drives whichever one it happens to read"
        )
        assert entry.landed, (
            f"{entry.name} carries a planned_in again while its module is "
            f"importable; the countdown that expires a marker keys on the "
            f"module, so this is the state where a verb ships uncovered"
        )

    assert scan_entry.module_id == apply_entry.module_id == "adoption", (
        "the profile toggle is a different namespace from the package and was "
        "never the thing that was wrong"
    )


def test_no_landed_adoption_verb_still_owes_the_file_the_board_reads():
    """P5. ``scripts/board.py`` reads ``tests/_pending.py`` and nothing else.

    An obligation carried only by a ``planned_in`` marker on a CLOSING unit is
    owned by nobody the moment that unit closes: the board reports no drift and
    no contradiction, and the verb ships uncovered. That is R-13's failure, and it
    was live for three closed units.

    THIS GUARD USED TO ASSERT THE OBLIGATION WAS PRESENT, with the text of the
    register entry read for the words naming the wall. U27 landed
    ``cratekit.adopt.apply_cli`` and spent that entry, so the old assertion was a
    countdown that had reached zero. It is answered here rather than deleted, and
    the property it becomes is the one that holds in both directions and for
    every adoption verb this package ever adds: a verb that has not landed is
    registered, and a verb that HAS landed is not. The second half is the one
    that bites, because a register entry left behind after its module ships makes
    ``board.py audit`` exit 2 on a contradiction nobody introduced deliberately.

    WHAT THE SPENT ENTRY SAID, kept here because a fact deleted with its entry is
    a fact the next reader re-derives: R-13 named the wall as the absence of a
    database and that was wrong. It was two properties of ``test_conformance_3``,
    an inline answer against an ``explicit`` gate and a one-gate-per-drive loop
    against a verb declaring two. Both were fixed in the test, and the rider that
    outlived the entry is R-148.
    """
    from cratekit.cli import registry  # noqa: PLC0415
    from tests import _pending  # noqa: PLC0415

    for entry in registry.ENTRIES:
        if entry.module_id != "adoption":
            continue
        registered = entry.module in _pending.PENDING
        assert registered is not entry.landed, (
            f"{entry.name} has landed={entry.landed} and is "
            f"{'in' if registered else 'absent from'} the pending register. A "
            f"landed module still owed by the register is the contradiction "
            f"board.py audit exits 2 on; an unlanded one absent from it is an "
            f"obligation nobody owns"
        )
        if registered:
            unit, _what = _pending.PENDING[entry.module]
            assert unit == entry.planned_in, (
                "the marker and the register name two different units, so "
                "whichever one somebody reads is the one that is wrong"
            )


def test_the_adoption_shell_never_reaches_into_the_layer_above_it():
    """KTD23, at the one place in this package that wants to break it.

    A command-line shell wants ``registry.Entry`` for its builder signature, and
    ``cratekit/adopt/`` is the modules layer. Importing it would be a real cycle
    hidden behind a type annotation. The legal shape names
    :mod:`cratekit.cli.output` alone, which is foundation-ranked because KTD25
    reserves the output contract globally before any verb ships.
    """
    from tests.test_layering import import_direction_violations  # noqa: PLC0415

    problems: list[str] = []
    for path in sorted(ADOPT_ROOT.rglob("*.py")):
        module = (
            "cratekit.adopt"
            if path.stem == "__init__"
            else f"cratekit.adopt.{path.stem}"
        )
        problems += import_direction_violations(path.read_text(), module)
    assert not problems, problems

    # Named rather than merely ranked, because "no upward import" is satisfied
    # by a shell that imports nothing at all, and the trap here is specific: the
    # ONE cli module a shell is allowed to name is the output contract. Read
    # from the syntax tree rather than the text, so the docstring explaining the
    # trap does not answer for the code.
    imported = {
        node.module
        for node in ast.walk(ast.parse((ADOPT_ROOT / "scan_cli.py").read_text()))
        if isinstance(node, ast.ImportFrom) and node.module
    }
    imported |= {
        alias.name
        for node in ast.walk(ast.parse((ADOPT_ROOT / "scan_cli.py").read_text()))
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    reaching_up = {name for name in imported if name.startswith("cratekit.cli")}
    assert reaching_up == {"cratekit.cli.output"}, (
        f"the shell names {sorted(reaching_up)} from the CLI layer; the output "
        f"envelope is the only one that is foundation-ranked (KTD25)"
    )


def test_no_module_in_the_adoption_package_spells_a_taxonomy_display_name():
    """R19. A display name is code, config, a persisted key, and a folder at once."""
    from tests.test_layering import TAXONOMY_LITERALS

    offenders: list[str] = []
    for path in sorted(ADOPT_ROOT.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Constant) and node.value in TAXONOMY_LITERALS:
                offenders.append(f"{path.name}: {node.value!r}")
    assert not offenders, offenders


def test_the_plan_document_carries_identifiers_and_the_digest(cfg, declared):
    routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    document = adopt_plan.to_json(plan)
    assert document["digest"] == plan.digest()
    assert document["entries"][0]["bucket"] == routable
    assert document["entries"][0]["id"].startswith(adopt_plan.ENTRY_ID_PREFIX)
    assert set(document["counts"]) >= {str(m) for m in adopt_scan.Readability}
    # It is a transport, not an editing surface: it round trips through JSON.
    assert json.loads(json.dumps(document)) == document


def test_an_entry_identifier_moves_when_the_destination_moves(declared):
    """Otherwise a resume reports moved work as already done."""
    first = adopt_plan.entry_id_for(TREE_ID, "c1", "bucket_a", "sub_a")
    assert first == adopt_plan.entry_id_for(TREE_ID, "c1", "bucket_a", "sub_a")
    assert first != adopt_plan.entry_id_for(TREE_ID, "c1", "bucket_b", "sub_a")
    assert first != adopt_plan.entry_id_for(TREE_ID, "c1", "bucket_a", "sub_b")
    assert first != adopt_plan.entry_id_for("other_tree", "c1", "bucket_a", "sub_a")
    assert declared is not None


def test_every_plan_entry_identifier_is_derivable_from_the_record_it_names(cfg, declared):
    """An identifier nobody can recompute from the record is one nobody can audit.

    Derived over every entry rather than over the routable ones, because the
    first version of this hashed a bucket that the undeclared entries then did
    not carry: the value looked right, nothing failed, and a reader comparing
    the record against its own identifier would have found them disagreeing.
    """
    music = Path(cfg.library.root) / "Music"
    _routable, genre = _bucket_and_genre(declared)
    rows = [
        adopt_scan.CollectionRow("ok", str(music / "A.flac"), genre, False),
        adopt_scan.CollectionRow("blank", str(music / "B.flac"), "", False),
        adopt_scan.CollectionRow("stream", "provider:track:1", genre, False),
    ]
    plan = _plan_of(cfg, declared, rows)
    assert plan.entries
    for entry in plan.entries:
        assert entry.entry_id == adopt_plan.entry_id_for(
            entry.tree, entry.content_id, entry.bucket, entry.sub
        ), entry


def test_the_two_enumerations_the_counts_share_a_mapping_have_no_common_value():
    """The duplicate-key shape, asked of two enums instead of one literal.

    ``AdoptionPlan.counts`` builds one mapping out of ``Disposition`` and
    ``Readability``. A member added to either with a value the other already
    uses collapses two counts onto one key, and every test over the mapping
    iterates the runtime object and cannot see it.
    """
    dispositions = {str(member) for member in adopt_scan.Disposition}
    categories = {str(member) for member in adopt_scan.Readability}
    assert dispositions.isdisjoint(categories), sorted(dispositions & categories)
    assert len(adopt_plan.AdoptionPlan(tree=TREE_ID).counts()) == len(dispositions) + len(
        categories
    )
