"""U23: library adoption, from the census to the approval to the revert.

Adoption reads an existing library, proposes where each track belongs in the
declared taxonomy, and writes only what is approved, a piece at a time,
resuming where it stopped. The brief's six scenarios, and where each is proved:

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

Beside them: a collision's identity under a rename, the order of the writes per
entry and what a crash between two costs, both readers against every wrong
document, and the lock, proved by real processes. D1 applies to every name here.
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
from cratekit.adopt import revert_changed as adopt_changed
from cratekit.adopt import scan as adopt_scan
from cratekit.core import cause, config, locations, review, tags, taxonomy
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from tests._containers import synth_container
from tests.test_config import valid_data

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
ADOPT_ROOT = SRC_ROOT / "cratekit" / "adopt"

# ── synthesized names (D1) ───────────────────────────────────────────────────

TREE_ID = "shelf_stack"
HANDLER = "adopt.scan"

#: One name in each composition form, because the pair is the whole reason the identity primitives
#: exist and a ledger keyed on the raw string holds two records for one file.
COMPOSED = "Café One.flac"
DECOMPOSED = unicodedata.normalize("NFD", COMPOSED)


# Fixtures


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
    """A bucket the shipped template really declares, and a genre that reaches it."""
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


#: Each container's silence, synthesized by ffmpeg once per process and copied
#: after, so a test pays for a file copy rather than an encoder run.
_SYNTHESIZED: dict[str, bytes] = {}


def _synth(tmp_path: Path, suffix: str) -> Path:
    """One second of silence in ``suffix`` at ``tmp_path``, as ``synth_container`` makes it."""
    if suffix not in _SYNTHESIZED:
        _SYNTHESIZED[suffix] = synth_container(tmp_path, suffix).read_bytes()
    out = tmp_path / f"probe{suffix}"
    out.write_bytes(_SYNTHESIZED[suffix])
    return out


def _synth_in(directory: Path, suffix: str) -> Path:
    """``_synth`` into a directory that may not exist yet. It does not mkdir."""
    directory.mkdir(parents=True, exist_ok=True)
    return _synth(directory, suffix)


def _adopt(cfg_value, path, **kwargs):
    """Record and write one genre value the way an apply does, through the one locked call."""
    return adopt_revert.write_tag_with_record(cfg_value, path, field="genre", **kwargs)


def _readable(_path: Path) -> adopt_scan.Readability:
    """A probe that says every file is fine, for tests about something else."""
    return adopt_scan.Readability.READABLE


def _plan_of(cfg_value, declared_taxonomy, rows, *, existing=()) -> adopt_plan.AdoptionPlan:
    scanned = list(
        adopt_scan.scan_rows(rows, declared_taxonomy, root=cfg_value.library.root, probe=_readable)
    )
    return adopt_plan.build_adoption_plan(
        scanned, declared_taxonomy, tree=TREE_ID, existing=existing
    )


def _in_separate_processes(script: str, *, workers: int, arguments) -> None:
    """Run one short script in several REAL interpreters at once, and check each."""
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


# Scenario 1: every unreadable shape is a NAMED category, never an omission


def test_every_unreadable_shape_appears_as_its_own_named_category(cfg, declared, tmp_path):
    """AE12, and the reason it is an acceptance criterion rather than a nicety."""
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
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=probe))
    found = {track.content_id: track.readability for track in scanned}

    assert found[str(present)] is adopt_scan.Readability.READABLE
    assert found[str(evicted)] is adopt_scan.Readability.ONLINE_ONLY
    assert found[str(unreadable)] is adopt_scan.Readability.UNREADABLE
    assert found["gone"] is adopt_scan.Readability.MISSING
    assert found["elsewhere"] is adopt_scan.Readability.UNMAPPED
    assert found["stream"] is adopt_scan.Readability.NOT_A_PATH

    counts = adopt_scan.categories(scanned)
    assert set(counts) == {str(member) for member in adopt_scan.Readability}, (
        "the summary lists only the categories it happened to see"
    )
    assert counts[str(adopt_scan.Readability.ONLINE_ONLY)] == 1


def test_an_online_only_file_is_never_opened_by_the_probe(cfg, monkeypatch):
    """Opening a dataless file triggers a download, per file, across a library."""
    music = Path(cfg.library.root) / "Music"
    dataless = music / "Dataless.flac"
    dataless.write_bytes(b"audio")
    real_stat = Path.stat

    class _Stat:
        # THE LITERAL, not the constant the probe compares against.
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
    """The block count answered a question it was never asked, twice."""
    music = Path(cfg.library.root) / "Music"
    sparse = music / "Sparse.flac"
    with sparse.open("wb") as handle:
        handle.truncate(1024 * 1024)
    assert sparse.stat().st_blocks == 0 and sparse.stat().st_size > 0, (
        "this platform allocated blocks for a sparse file"
    )
    assert adopt_scan.probe_readability(sparse) is adopt_scan.Readability.READABLE


def test_a_stale_placeholder_beside_a_readable_file_does_not_hide_it(cfg):
    """A stub is debris as often as it is evidence, and the file decides."""
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
    """Totality is claimed as a property of THIS function, so drive this function."""
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
    """Totality is a property of the PROBE, not of the inputs it is lucky with."""
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
        scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root))
    finally:
        os.chmod(locked, 0o755)

    assert len(scanned) == len(rows), (
        "the census stopped part way and every row after it is a track nobody decided about, with no count anywhere saying so"
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
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=hostile))
    assert len(scanned) == 5
    assert {track.readability for track in scanned} == {adopt_scan.Readability.UNREADABLE}


@pytest.mark.parametrize("spelling", ["localhost", "empty-authority"])
def test_a_row_recorded_THE_WAY_REKORDBOX_RECORDS_ONE_is_adoptable(cfg, declared, spelling):
    """The census against the shape a real library holds, not the assumed one."""
    music = Path(cfg.library.root) / "Music"
    present = music / "Recorded.flac"
    present.write_bytes(b"audio")
    _routable, genre = _bucket_and_genre(declared)
    recorded = (
        locations.location_url(present) if spelling == "localhost" else "file://" + str(present)
    )
    assert not recorded.startswith("/"), "the fixture built a path, not a location"

    rows = [adopt_scan.CollectionRow("c1", recorded, genre, False)]
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root))
    assert scanned[0].readability is adopt_scan.Readability.READABLE
    assert scanned[0].disposition is adopt_scan.Disposition.ROUTE
    assert scanned[0].path == str(present)

    plan = adopt_plan.build_adoption_plan(scanned, declared, tree=TREE_ID)
    assert len(plan.applicable()) == 1, "the plan covers every row and can apply none of them"
    assert adopt_plan.covers(plan, scanned) == frozenset(), (
        "coverage was satisfied by the broken build too"
    )


def test_a_location_naming_another_host_is_reported_rather_than_guessed(cfg, declared):
    """The decoder refuses a remote authority, and the census must not die on it."""
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
        "every row came back not-a-path"
    )


def test_a_row_whose_location_column_is_NULL_does_not_end_the_census(cfg, declared):
    """A null ``FolderPath`` is an ordinary rekordbox row."""
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
    """Refusing what can be coerced is the same defect as raising on it."""
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
    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=_readable))
    assert [track.content_id for track in scanned] == ["live"]


def test_a_row_that_cannot_report_its_soft_delete_marker_is_a_construction_error():
    """``deleted`` has no default, so a producer cannot supply the permissive one."""
    with pytest.raises(TypeError):
        adopt_scan.CollectionRow("id", "/x/y.flac", "House")  # type: ignore[call-arg]


# Scenario 2: the third population has a declared disposition, always


@pytest.mark.parametrize("genre", ["", "   ", None])
def test_a_blank_or_generic_genre_gets_a_disposition(declared, genre):
    disposition, bucket, _match = adopt_scan.classify_genre(declared, genre or "")
    assert disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert bucket == ""


def test_a_genre_the_taxonomy_calls_too_coarse_gets_a_disposition(declared):
    """Asked of the template rather than of a list here."""
    coarse = declared.fallback.too_coarse_as_source
    assert coarse, "the shipped template declares nothing too coarse to be a source"
    for value in coarse:
        disposition, bucket, _ = adopt_scan.classify_genre(declared, value)
        assert disposition is adopt_scan.Disposition.NEEDS_GENRE, value
        assert bucket == ""


def test_the_fallback_tier_is_never_accepted_as_an_adoption_answer(declared):
    """Approach point 2, and the defect it was caught as."""
    resolution = adopt_scan.routing.resolve_bucket(declared, "a genre nobody declares")
    assert resolution.match is adopt_scan.routing.Match.FALLBACK
    assert resolution.bucket_id == declared.fallback.bucket

    disposition, bucket, _ = adopt_scan.classify_genre(declared, "a genre nobody declares")
    assert disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert bucket == ""


def test_the_plan_carries_every_scanned_row_whatever_happened_to_it(cfg, declared):
    """The strong form: a set comparison, not a count."""
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

    scanned = list(adopt_scan.scan_rows(rows, declared, root=cfg.library.root, probe=probe))
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
    review.resolve(store, first[0], review.Verdict.ACCEPTED, option=chosen, actor="tester")

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
        "answering a question changed the plan and the digest did not move"
    )


def test_an_answer_naming_an_undeclared_bucket_is_ignored(cfg, declared):
    """It can only arrive from a verdict recorded against a template that moved."""
    music = Path(cfg.library.root) / "Music"
    rows = [adopt_scan.CollectionRow("blank", str(music / "A.flac"), "", False)]
    plan = _plan_of(cfg, declared, rows)
    answered = adopt_plan.with_verdicts(plan, {"blank": "no_such_bucket"}, declared)
    assert answered.entries[0].disposition is adopt_scan.Disposition.NEEDS_GENRE
    assert answered.applicable() == ()


# Scenario 6: a folder that is already there is surfaced, not merged


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
    """The question was asked and NOTHING READ THE ANSWER, which is worse than not asking."""
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
        "the person said to leave the folder alone and adoption still has work queued for it"
    )
    assert {entry.disposition for entry in left_alone.entries} == {adopt_scan.Disposition.WITHHELD}
    assert adopt_plan.covers(left_alone, []) == frozenset()
    assert len(left_alone.entries) == len(plan.entries), (
        "a withheld track fell out of the plan instead of being carried with a name that says why"
    )
    assert left_alone.digest() != plan.digest(), (
        "answering the collision changed the plan and the digest did not move"
    )

    merged = adopt_plan.with_collision_verdicts(plan, {"node-41": adopt_plan.COLLISION_ADOPT})
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
        existing=[adopt_plan.ExistingFolder("node-41", declared.bucket(routable).display, ("x",))],
    )
    withheld = adopt_plan.with_collision_verdicts(plan, {"node-41": adopt_plan.COLLISION_SEPARATE})
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
    """P7. A guard that fires on the ordinary case is a guard people route around."""
    routable, genre = _bucket_and_genre(declared)
    rows = [_row(cfg, "A.flac", genre, "a")]
    existing = [
        adopt_plan.ExistingFolder(
            node_id="node-41", display=declared.bucket(routable).display, content_ids=("a",)
        )
    ]
    assert _plan_of(cfg, declared, rows, existing=existing).collisions == ()


def test_a_collision_is_addressed_by_the_node_and_survives_a_rename(cfg, declared, store):
    """THE DEFECT U19 SHIPPED, one layer earlier, and it was blocking there."""
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
    renamed_declared = _taxonomy_with_bucket_display(declared, routable, "Renamed Shelf")
    after = adopt_plan.ExistingFolder("node-41", "Renamed Shelf", ("a", "stranger"))
    replanned = _plan_of(cfg, renamed_declared, rows, existing=[after])
    second = adopt_plan.offer_plan(
        replanned_store := store, replanned, renamed_declared, handler_key=HANDLER
    )

    assert second[-1] == first[-1], (
        "the renamed folder produced a second review item for one library node"
    )
    settled = review.get(replanned_store, second[-1])
    assert settled.verdict is review.Verdict.ACCEPTED
    assert settled.payload["node_id"] == "node-41"
    # The payload of a SETTLED item is deliberately not refreshed by a re-offer, so what
    # is on record is what the person was looking at when they decided.
    assert settled.payload["display"] == display


def _taxonomy_with_bucket_display(declared, bucket_id: str, display: str):
    """The same template with one bucket renamed, REBUILT THROUGH THE LOADER."""
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


# Scenario 4: R34. Nothing blanket applies a plan


BLANKET_SHAPES = [
    True,
    1,
    "yes",
    "approve",
    {"approved": True},
    {"digest": "anything", "actor": "somebody", "option": "approve"},
    None,
]


@pytest.mark.parametrize(
    "blanket", BLANKET_SHAPES, ids=lambda v: str(type(v).__name__) + str(v)[:12]
)
def test_no_blanket_affirmative_applies_a_plan(cfg, declared, blanket):
    """R34, checked at RUNTIME rather than in the type checker."""
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
        "a refused apply left a ledger behind, so the refusal had already written something"
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
    """Every place a source reads a process environment variable."""
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
    """P7's half that keeps getting skipped: run the guard against the evasion."""
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
    """R34 as a structural property rather than a promise."""
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


# Scenario 3: applied thirty percent through, resumed from item thirty one


def _hundred(cfg_value, declared_taxonomy) -> adopt_plan.AdoptionPlan:
    _routable, genre = _bucket_and_genre(declared_taxonomy)
    rows = [_row(cfg_value, f"Track {n:03d}.flac", genre, f"c{n:03d}") for n in range(1, 101)]
    return _plan_of(cfg_value, declared_taxonomy, rows)


def test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one(cfg, declared):
    """The brief's third scenario, driven through a real interruption."""
    plan = _hundred(cfg, declared)
    granted = adopt_approval.grant(plan, actor="tester")
    wrote: list[str] = []

    def place(entry, _folder, _sub):
        if len(wrote) == 30:
            # A KILL, not a refusal.
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
    """The order U19 established, and the one direction that is not recoverable."""
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
    """R19: the record keys on identifiers and the names are resolved from the template."""
    routable, genre = _bucket_and_genre(declared)
    plan = _plan_of(cfg, declared, [_row(cfg, "A.flac", genre, "a")])
    entry = plan.applicable()[0]
    assert declared.bucket(routable).display not in (entry.bucket, entry.sub)

    mapping = adopt_apply.membership_plan(plan.applicable(), declared)
    assert list(mapping) == [adopt_apply.destination(declared, entry.bucket, entry.sub)]
    assert list(mapping.values()) == [["a"]]

    renamed = _taxonomy_with_bucket_display(declared, routable, "Renamed Shelf")
    remapped = adopt_apply.membership_plan(plan.applicable(), renamed)
    assert list(remapped)[0][0] == "Renamed Shelf"


def test_an_entry_whose_destination_the_template_dropped_costs_one_entry(cfg, declared):
    """PER ENTRY, never out of the pass. U19 paid for this one."""
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
    scanned = list(adopt_scan.scan_rows(rows, declared_taxonomy, root=tmp_path, probe=_readable))
    assert cfg_value is not None
    return adopt_plan.build_adoption_plan(scanned, declared_taxonomy, tree=TREE_ID)


def test_a_refusal_from_the_writer_rewrites_no_files_at_all(cfg, declared, tmp_path):
    """The gates in front of a destructive run are DOWNSTREAM of this write."""
    plan = _plan_over_real_files(cfg, declared, tmp_path, [".flac"] * 6)
    assert len(plan.applicable()) == 6

    def refusing_place(*_args):
        raise cause.refuse("decision-required", "the backup acknowledgment has not been answered")

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
            "a refused run rewrote the genre tag on a user's file"
        )
    assert adopt_revert.read(cfg).snapshots == (), (
        "a refused run left revert records, so it had already touched files"
    )
    assert report.applied == ()
    assert adopt_apply.read(cfg).applied == ()
    # REPORTED ONCE PER ENTRY, and that is correct rather than tolerated.
    assert set(report.failed) == {entry.entry_id for entry in plan.applicable()}


def test_a_refusal_about_one_track_still_costs_only_that_track(cfg, declared, tmp_path):
    """The other direction, so the fix is not "stop on everything" (P7)."""
    plan = _plan_over_real_files(cfg, declared, tmp_path, [".flac"] * 6)
    refused = plan.applicable()[0].entry_id
    attempted: list[str] = []

    def place(entry, _folder, _sub):
        attempted.append(entry.entry_id)
        if entry.entry_id == refused:
            raise cause.refuse("internal-error", "this one row has no collection entry")

    report = adopt_apply.apply_plan(
        cfg,
        plan,
        declared,
        approval=adopt_approval.grant(plan, actor="tester"),
        place=place,
        tag_value=lambda *_: "Adopted Genre",
    )
    assert len(attempted) == 6, (
        f"only {len(attempted)} of 6 entries were attempted; one row's refusal ended the pass"
    )
    assert len(report.applied) == 5 and list(report.failed) == [refused]
    for entry in plan.applicable():
        if entry.entry_id == refused:
            continue
        assert tags.read_genre_from_file(Path(entry.path)) == "Adopted Genre"


def test_a_track_DELETED_between_the_census_and_the_apply_costs_one_entry(cfg, declared, tmp_path):
    """The ledger keys a record on the file's identity, so a vanished file cannot be recorded."""
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
        f"only {len(attempted)} of 4 entries were attempted; one deleted track ended the pass"
    )
    assert list(report.failed) == [gone.entry_id], report.failed
    assert "cannot be identified on this machine" in report.failed[gone.entry_id]
    assert len(report.applied) == 3
    assert (
        adopt_revert.read(cfg).snapshot(adopt_revert.identity_of(Path(entries[0].path)), "genre")
        is not None
    )
    for entry in entries:
        if entry.entry_id == gone.entry_id:
            continue
        assert tags.read_genre_from_file(Path(entry.path)) == "Adopted Genre"


def test_a_record_is_never_written_for_a_file_that_cannot_be_identified(cfg, tmp_path):
    """The refusal itself, and that it is a refusal rather than a fallback."""
    missing = tmp_path / "not-here.flac"
    with pytest.raises(adopt_revert.AdoptedFileUnidentifiable) as refused:
        _adopt(cfg, missing, written="Adopted", entry_id="e1")
    assert refused.value.cause.reason == "adoption-file-unidentifiable"
    assert REASONS["adoption-file-unidentifiable"] is ExitCode.PRECONDITION
    assert refused.value.cause.scope is cause.Scope.ITEM
    assert adopt_revert.read(cfg).snapshots == (), (
        "a record was written for a file this build cannot identify"
    )


def test_a_container_this_build_cannot_write_costs_one_entry_not_the_run(cfg, declared, tmp_path):
    """``write_tags`` raises ``UnsupportedContainer`` from OUTSIDE its own try."""
    plan = _plan_over_real_files(cfg, declared, tmp_path, [".flac", ".flac", ".aac", ".flac"])
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
    assert not any(record.path.endswith(".aac") for record in adopt_revert.read(cfg).snapshots), (
        "a revert record was left for a file whose tag was never written"
    )

    # AND IT NEVER RECEIVED A MEMBERSHIP EITHER.
    assert awkward.entry_id not in placed, (
        "the entry this build cannot finish still had its membership written"
    )
    assert len(placed) == 3, "3 is the full complement here"

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


# Scenario 5: a tag write is reverted EXACTLY


def test_a_tag_write_is_reverted_exactly(cfg, tmp_path):
    """The value that was there before comes back, byte for byte."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")

    _adopt(cfg, path, written="Adopted Genre", entry_id="e1")
    assert tags.read_genre_from_file(path) == "Adopted Genre"

    report = adopt_revert.revert_tags(cfg)
    assert report.restored == ((str(path), "genre"),)
    assert report.failed == {}
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert adopt_revert.read(cfg).snapshots == ()


def test_an_absent_tag_is_reverted_to_ABSENT_and_not_to_an_empty_string(cfg, tmp_path):
    """ "Exactly" includes absence, and the tag writer cannot express it."""
    path = _synth(tmp_path, ".flac")
    assert tags.read_genre_from_file(path) is None

    _adopt(cfg, path, written="Adopted Genre", entry_id="e1")
    adopt_revert.revert_tags(cfg)
    assert tags.read_genre_from_file(path) is None


def test_the_original_is_recorded_before_the_file_is_touched(cfg, declared, tmp_path):
    """The seam where the reverse order loses a value nothing can put back."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _routable, genre = _bucket_and_genre(declared)
    row = adopt_scan.CollectionRow(str(path), str(path), genre, False)
    scanned = list(adopt_scan.scan_rows([row], declared, root=tmp_path, probe=_readable))
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
    """The crash between the tag write and the applied record, and why it is safe."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted Genre")

    again, _landed = _adopt(cfg, path, written="Adopted Genre")
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
    """A ledger keyed on the file alone restores one field and keeps the other's new value."""
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
    """The primitive U31 exists for, and the cost of not using it here."""
    assert COMPOSED != DECOMPOSED
    directory = tmp_path / "accented"
    directory.mkdir()
    composed = _synth(directory, ".flac")
    composed = composed.rename(directory / COMPOSED)
    tags.write_genre(composed, "User Genre")
    decomposed = directory / DECOMPOSED

    _adopt(cfg, composed, written="Adopted", entry_id="e1")
    _adopt(cfg, decomposed, written="Adopted", entry_id="e2")

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.path for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)


def test_one_file_under_TWO_HARD_LINKS_is_one_record(cfg, tmp_path):
    """Two names, one inode, and the ledger used to hold two originals for it."""
    first = _synth(tmp_path, ".flac")
    tags.write_genre(first, "User Genre")
    second = tmp_path / "second-name.flac"
    os.link(first, second)
    assert first.stat().st_ino == second.stat().st_ino

    _adopt(cfg, first, written="Adopted Bucket", entry_id="e1")
    _adopt(cfg, second, written="Adopted Bucket", entry_id="e2")

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [(entry.path, entry.original) for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",), (
        "the second record recorded adoption's own value as the original"
    )
    assert ledger.snapshots[0].path == str(first), (
        "the recorded address was moved to the second name for no reason"
    )
    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(first) == "User Genre"


def test_TWO_CASE_SPELLINGS_are_one_record_or_two_exactly_as_the_VOLUME_says(cfg, tmp_path):
    """The defect on the volume format this product targets, and its mirror."""
    upper = tmp_path / "SongZero.flac"
    _synth(tmp_path, ".flac").rename(upper)
    lower = tmp_path / "songzero.flac"
    one_file = lower.exists()
    if not one_file:
        _synth_in(tmp_path / "src", ".flac").rename(lower)
        tags.write_genre(lower, "Lower Genre")
    tags.write_genre(upper, "Upper Genre")

    _adopt(cfg, upper, written="Adopted Bucket", entry_id="e1")
    _adopt(cfg, lower, written="Adopted Bucket", entry_id="e2")

    originals = {entry.original for entry in adopt_revert.read(cfg).snapshots}
    if one_file:
        assert originals == {("Upper Genre",)}, originals
        assert adopt_revert.revert_tags(cfg).failed == {}
        assert tags.read_genre_from_file(upper) == "Upper Genre"
    else:
        assert originals == {("Upper Genre",), ("Lower Genre",)}, originals


def test_TWO_VOLUMES_that_allocate_the_SAME_INODE_NUMBER_stay_two_records(cfg, tmp_path):
    """An inode number is unique to a volume and to nothing wider than that."""
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
        _adopt(cfg, first, written="Adopted Bucket", entry_id="e1")
        _adopt(cfg, second, written="Adopted Bucket", entry_id="e2")
    finally:
        Path.stat = real_stat

    originals = {entry.original for entry in adopt_revert.read(cfg).snapshots}
    assert originals == {("Internal Genre",), ("External Genre",)}, originals


def test_a_file_RENAMED_between_two_adoptions_is_still_one_record(cfg, tmp_path):
    """The third spelling of one file, and the one the path digest never saw."""
    before = _synth(tmp_path, ".flac")
    tags.write_genre(before, "User Genre")
    _adopt(cfg, before, written="Adopted", entry_id="e1")
    after = tmp_path / "renamed.flac"
    before.rename(after)
    _adopt(cfg, after, written="Adopted", entry_id="e2")

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.path for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].path == str(after), (
        "the record still points at a name that is not there"
    )
    assert adopt_revert.revert_tags(cfg).failed == {}
    assert tags.read_genre_from_file(after) == "User Genre"


def test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled(cfg, tmp_path):
    """An upgrade must not be a second identity for a file that already has one."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    legacy = hashlib.sha256(locations.location_to_path(str(path)).encode("utf-8")).hexdigest()[:24]
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

    _adopt(cfg, path, written="Adopted", entry_id="e1")
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.file for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].file == adopt_revert.identity_of(path)
    assert ledger.snapshots[0].written_by("e0")
    assert ledger.snapshots[0].written_by("e1")


def test_a_legacy_record_that_is_the_only_one_for_its_file_still_reverts(cfg, tmp_path):
    """The direction an over-tightened identity check would have broken."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Adopted")
    legacy = hashlib.sha256(locations.location_to_path(str(path)).encode("utf-8")).hexdigest()[:24]
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


# The identity is a CORROBORATION, and every disagreement is a refusal


class _Renumbered:
    """One file's ``stat`` with the volume and inode a filesystem event moved."""

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
    """The defect the previous round shipped, driven end to end."""
    first = _synth_in(tmp_path / "a", ".flac")
    tags.write_genre(first, "Real Genre A")
    _adopt(cfg, first, written="Adopted Bucket", entry_id="e1")
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.original == ("Real Genre A",)

    second = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(second, "Real Genre B")
    recycled = first.stat().st_ino
    first.unlink()
    _stat_reporting(monkeypatch, second, st_dev=held_dev(held), st_ino=recycled)
    assert adopt_revert.identity_of(second) == held.file

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        _adopt(cfg, second, written="Adopted Bucket", entry_id="e2")
    assert "inode number is REUSED" in refused.value.cause.message
    assert refused.value.cause.remediation.remedy is Remedy.RUN_DOCTOR

    assert tags.read_genre_from_file(second) == "Real Genre B", (
        "adoption wrote to a file whose original it had not recorded"
    )
    assert adopt_revert.read(cfg).snapshots == (held,), (
        "the record moved, so one file's original is now filed under another file's name"
    )

    # AND THE REVERT CANNOT REACH B EITHER.
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), report.restored
    assert report.failed == {(str(first), "genre"): "the file is no longer there"}
    assert tags.read_genre_from_file(second) == "Real Genre B"


def held_dev(record) -> int:
    """The volume number a ``dev-ino`` record is keyed to."""
    return int(record.file.split(":")[1])


def test_a_recorded_path_is_NEVER_REFRESHED_to_a_DIFFERENT_files_path(cfg, tmp_path, monkeypatch):
    """The one line that turned a collision into a data loss, pinned on its own."""
    first = _synth_in(tmp_path / "a", ".flac")
    tags.write_genre(first, "Real Genre A")
    _adopt(cfg, first, written="Adopted Bucket", entry_id="e1")
    held = adopt_revert.read(cfg).snapshots[0]

    second = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(second, "Real Genre B")
    recycled = first.stat().st_ino
    first.unlink()
    _stat_reporting(monkeypatch, second, st_dev=held_dev(held), st_ino=recycled)

    with pytest.raises(adopt_revert.RecordCannotBeMatched):
        _adopt(cfg, second, written="Adopted Bucket", entry_id="e2")
    assert adopt_revert.read(cfg).snapshots[0].path == str(first), (
        "the recorded path was refreshed to a different file's path"
    )
    assert adopt_revert.read(cfg).snapshots[0].file == held.file
    assert adopt_revert.read(cfg).snapshots[0].original == ("Real Genre A",)


def test_an_os_replace_SAVE_does_not_produce_a_SECOND_record(cfg, tmp_path):
    """The inode moves for a file nobody replaced, and every tagger does it."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
    before = path.stat().st_ino

    saving = tmp_path / "saving.flac"
    saving.write_bytes(path.read_bytes())
    tags.write_tags(saving, {"title": "Retagged Elsewhere"})
    os.replace(saving, path)
    assert path.stat().st_ino != before, "the fixture did not move the inode"

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    assert "renames it over the original" in refused.value.cause.message

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [(entry.file, entry.original) for entry in ledger.snapshots]
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
    """Both halves of the pair move for an untouched file, and all three were measured."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
    first = adopt_revert.read(cfg).snapshots[0]

    _stat_reporting(monkeypatch, path, **moved)
    assert adopt_revert.identity_of(path) != first.file, "the fixture moved nothing"
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [(entry.file, entry.original) for entry in ledger.snapshots]
    settled = ledger.snapshots[0]
    assert settled.original == ("User Genre",)
    assert settled.file == adopt_revert.identity_of(path), (
        "the record kept a key naming numbers this file no longer has"
    )
    assert settled.path == str(path)
    assert settled.written_by("e1") and settled.written_by("e2")


def test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled(cfg, tmp_path):
    """The rename is one of the three spellings this whole round exists to handle."""
    before = _synth(tmp_path, ".flac")
    tags.write_genre(before, "Adopted Bucket")
    _legacy_ledger(cfg, (before, "User Genre", hashlib.sha256(before.read_bytes()).hexdigest()))
    assert len(adopt_revert.read(cfg).snapshots) == 1

    after = tmp_path / "renamed.flac"
    before.rename(after)
    _adopt(cfg, after, written="Adopted Bucket", entry_id="e1")

    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.file, entry.path, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",), (
        "the second record stored adoption's own value as the original"
    )
    assert ledger.snapshots[0].path == str(after)
    assert ledger.snapshots[0].file == adopt_revert.identity_of(after)

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(after) == "User Genre"


def test_TWO_RECORDS_claiming_one_file_by_DIFFERENT_evidence_refuse(cfg, tmp_path):
    """A ledger that contradicts itself is never resolved by preferring one claim."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    stray = dict(document["snapshots"][0])
    stray["file"] = "c" * 24
    stray["original"] = ["Some Other Original"]
    document["snapshots"][0]["path"] = str(tmp_path / "elsewhere.flac")
    document["snapshots"].append(stray)
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    assert len(adopt_revert.read(cfg).snapshots) == 2

    with pytest.raises(adopt_revert.RecordCannotBeMatched) as refused:
        _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    assert "claimed by two different records" in refused.value.cause.message
    assert len(adopt_revert.read(cfg).snapshots) == 2


def test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING(cfg, tmp_path, monkeypatch):
    """The corroboration is paid for only where a claim actually diverges."""
    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    monkeypatch.setattr(
        adopt_changed, "digest_of", lambda p, **kw: (reads.append(p), real_digest(p))[1]
    )
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")

    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
    # One read, and it is the stamp AFTER the write rather than a lookup.
    assert reads == [path], reads

    reads.clear()
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    assert reads == [path], (
        f"a re-run whose identity and path agree read the file to decide "
        f"something that was not in doubt, reads={reads}"
    )
    assert len(adopt_revert.read(cfg).snapshots) == 1

    # A SECOND FILE, INTO A LEDGER THAT ALREADY HOLDS A STAMPED RECORD.
    second = _synth_in(tmp_path / "second", ".flac")
    tags.write_genre(second, "Another User Genre")
    reads.clear()
    _adopt(cfg, second, written="Adopted Bucket", entry_id="e3")
    assert reads == [second], (
        f"the second file into a non-empty ledger was hashed to look itself up "
        f"and then hashed again to stamp it, which doubles the reads of the one "
        f"pass that touches every track in the library, reads={reads}"
    )
    assert len(adopt_revert.read(cfg).snapshots) == 2


def test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN(
    cfg, tmp_path, monkeypatch
):
    """The headline cost, counted per file rather than asserted in a docstring."""
    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    monkeypatch.setattr(
        adopt_changed, "digest_of", lambda p, **kw: (reads.append(p), real_digest(p))[1]
    )

    per_file: list[int] = []
    for index in range(8):
        track = _synth_in(tmp_path / f"track{index}", ".flac")
        tags.write_genre(track, f"User Genre {index}")
        reads.clear()
        _adopt(cfg, track, written="Adopted Bucket", entry_id=f"e{index}")
        per_file.append(len(reads))

    assert per_file == [1] * 8, (
        f"a first adoption into an empty ledger read some file more than once "
        f"per track, which is the whole-library pass paying twice: {per_file}"
    )
    assert sum(per_file) == 8
    assert len(adopt_revert.read(cfg).snapshots) == 8


def test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record(cfg, tmp_path):
    """A path that will not resolve because its VOLUME is absent is not a deletion."""
    volume = tmp_path / "Volumes" / "PORTABLE"
    on_the_volume = _synth_in(volume, ".flac")
    tags.write_genre(on_the_volume, "Volume Own Genre")

    _adopt(cfg, on_the_volume, written="Adopted Bucket", entry_id="e1")
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.original == ("Volume Own Genre",)
    assert held.digest_state is adopt_revert.DigestState.RECORDED

    # The backup is byte for byte what adoption left, which is the whole point of
    # a backup and is exactly the evidence the byte search accepts.
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    backup = backup_dir / "probe.flac"
    backup.write_bytes(on_the_volume.read_bytes())
    assert hashlib.sha256(backup.read_bytes()).hexdigest() == held.digest, (
        "the fixture did not produce a byte identical copy"
    )

    # DETACHED. Nothing was deleted; the volume is simply not there.
    for leftover in sorted(volume.iterdir()):
        leftover.unlink()
    volume.rmdir()
    assert not Path(held.path).exists()

    _adopt(cfg, backup, written="Adopted Bucket", entry_id="e2")
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 2, [(entry.path, entry.original) for entry in ledger.snapshots]
    kept = [entry for entry in ledger.snapshots if entry.path == held.path]
    assert kept == [held], "the copy took the record of a file whose volume was merely unplugged"
    # AND THE BACKUP GETS ITS OWN RECORD, recording what the BACKUP held, which is
    # adoption's value because a copy of an adopted file holds an adopted file's tag.
    taken = [entry for entry in ledger.snapshots if entry.path == str(backup)]
    assert len(taken) == 1 and taken[0].original == ("Adopted Bucket",), taken

    # REPLUGGED. The record is still the volume file's, so a re-adoption finds it
    # rather than writing adoption's own value down as the original.
    volume.mkdir(parents=True)
    Path(held.path).write_bytes(backup.read_bytes())
    _adopt(cfg, Path(held.path), written="Adopted Bucket", entry_id="e3")
    settled = [entry for entry in adopt_revert.read(cfg).snapshots if entry.path == held.path]
    assert len(settled) == 1 and settled[0].original == ("Volume Own Genre",), (
        f"the replugged file's original is no longer recorded anywhere: {settled}"
    )


def test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped(cfg, tmp_path):
    """Two agreeing addresses settle WHICH FILE, and settle nothing about content."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "A Own Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
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
        _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    assert "not the ones adoption left" in refused.value.cause.message
    assert "B Own Genre" in refused.value.cause.message
    assert "doctor" not in refused.value.cause.message

    assert tags.read_genre_from_file(path) == "B Own Genre", (
        "adoption wrote over a value it had not recorded"
    )
    assert adopt_revert.read(cfg).snapshots == (first,), (
        "the record was re-stamped from a different recording's bytes"
    )


def test_a_TAG_EDITED_IN_PLACE_is_still_accepted_because_nothing_is_at_risk(cfg, tmp_path):
    """The other half of the decision, and the reason it is not just "bytes moved"."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
    stamped = adopt_revert.read(cfg).snapshots[0]

    tags.write_tags(path, {"title": "Edited In A Tagging Session"})
    assert hashlib.sha256(path.read_bytes()).hexdigest() != stamped.digest, (
        "the fixture did not change the bytes, so this proves nothing"
    )
    assert path.stat().st_ino == Path(stamped.path).stat().st_ino

    _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [(entry.file, entry.original) for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].written_by("e1") and ledger.snapshots[0].written_by("e2")

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "User Genre"


def test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field(cfg, tmp_path):
    """The clause that reads the RECORD's ``written``, driven where it is the only one."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Bucket Alpha", entry_id="e1")
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.written == "Bucket Alpha"

    tags.write_tags(path, {"title": "Edited In A Tagging Session"})
    assert hashlib.sha256(path.read_bytes()).hexdigest() != held.digest

    _adopt(cfg, path, written="Bucket Beta", entry_id="e2")
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.written, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert tags.read_genre_from_file(path) == "Bucket Beta"


def test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write(cfg, tmp_path):
    """The clause that reads THIS CALL's value, and why the record's is not enough."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Bucket Alpha", entry_id="e1")
    _adopt(cfg, path, written="Bucket Beta", entry_id="e2")
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.written == "Bucket Alpha", "the record's written is not the stale one"
    assert tags.read_genre_from_file(path) == "Bucket Beta"

    tags.write_tags(path, {"title": "Edited In A Tagging Session"})
    assert hashlib.sha256(path.read_bytes()).hexdigest() != held.digest

    _adopt(cfg, path, written="Bucket Beta", entry_id="e3")
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [
        (entry.written, entry.original) for entry in ledger.snapshots
    ]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].written_by("e3")


def test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH(
    cfg, tmp_path, monkeypatch
):
    """The size shortcut cannot change an answer, so only a read COUNT can see it."""
    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    monkeypatch.setattr(
        adopt_changed, "digest_of", lambda p, **kw: (reads.append(p), real_digest(p))[1]
    )

    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
    held = adopt_revert.read(cfg).snapshots[0]

    # LONGER BY CONSTRUCTION.
    saving = tmp_path / "saving.flac"
    saving.write_bytes(path.read_bytes() + b"\x00" * 4096)
    os.replace(saving, path)
    assert path.stat().st_size != held.size, "the fixture did not move the size"

    reads.clear()
    with pytest.raises(adopt_revert.RecordCannotBeMatched):
        _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    assert reads == [], (
        f"a record whose recorded size is not this file's size was corroborated "
        f"by hashing the whole file, which no answer could depend on: {reads}"
    )


def test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger(cfg, tmp_path):
    """The hardlink shape returned before the byte check, so it never reached one."""
    first = _synth(tmp_path, ".flac")
    tags.write_genre(first, "User Genre")
    second = tmp_path / "second-name.flac"
    os.link(first, second)

    _adopt(cfg, first, written="Adopted Bucket", entry_id="e1")
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
        _adopt(cfg, second, written="Adopted Bucket", entry_id="e2")
    assert "Stranger Own Genre" in refused.value.cause.message
    assert adopt_revert.read(cfg).snapshots == (held,)
    assert tags.read_genre_from_file(second) == "Stranger Own Genre"


def test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut(cfg, tmp_path):
    """The size can rule a record out and can never rule one in, so pin the digest."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "A Own Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
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
        _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    assert "not the ones adoption left" in refused.value.cause.message
    assert adopt_revert.read(cfg).snapshots == (held,)


def test_TWO_RECORDS_for_ONE_FILE_AND_FIELD_never_reach_the_lookup_at_all(cfg, tmp_path):
    """The cell a hardlinked second path used to be able to write."""
    first = _synth(tmp_path, ".flac")
    tags.write_genre(first, "User Genre")
    second = tmp_path / "second-name.flac"
    os.link(first, second)
    _adopt(cfg, first, written="Adopted Bucket", entry_id="e1")

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
        _adopt(cfg, second, written="Adopted Bucket", entry_id="e2")
    assert tags.read_genre_from_file(first) == "Adopted Bucket"


def test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED(cfg, tmp_path):
    """Every message here ended by naming a command the build does not have."""
    from cratekit.cli import registry as cli_registry

    planned = {one.name for one in cli_registry.entries() if one.planned_in}
    assert "doctor" not in planned, (
        "doctor is planned again, which would make the U27 merge's discharge of the cratekit.cli.doctor countdown entry wrong"
    )

    said: list[str] = []

    replaced = _synth(tmp_path, ".flac")
    tags.write_genre(replaced, "A Own Genre")
    _adopt(cfg, replaced, written="Adopted Bucket", entry_id="e1")
    other = _synth_in(tmp_path / "b", ".flac")
    tags.write_genre(other, "B Own Genre")
    with replaced.open("r+b") as handle:
        handle.truncate(0)
        handle.write(other.read_bytes())
    with pytest.raises(adopt_revert.RecordCannotBeMatched) as value_refusal:
        _adopt(cfg, replaced, written="Adopted Bucket", entry_id="e2")
    said.append(value_refusal.value.cause.message)

    saved = _synth_in(tmp_path / "saved", ".flac")
    tags.write_genre(saved, "User Genre")
    _adopt(cfg, saved, written="Adopted Bucket", entry_id="e3")
    moving = tmp_path / "moving.flac"
    moving.write_bytes(saved.read_bytes())
    tags.write_tags(moving, {"title": "Retagged Elsewhere"})
    os.replace(moving, saved)
    with pytest.raises(adopt_revert.RecordCannotBeMatched) as path_refusal:
        _adopt(cfg, saved, written="Adopted Bucket", entry_id="e4")
    said.append(path_refusal.value.cause.message)

    assert len(said) == 2
    for message in said:
        named = sorted(verb for verb in planned if verb in message)
        assert not named, f"a refusal names a verb this build does not have: {named} in {message!r}"
        assert "Run the" not in message, message


def test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file(cfg, tmp_path):
    """The re-run the whole module exists for must not need a digest."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted Bucket", entry_id="e1"
    )
    held = adopt_revert.read(cfg).snapshots[0]
    assert held.digest_state is adopt_revert.DigestState.ABSENT

    _adopt(cfg, path, written="Adopted Bucket", entry_id="e2")
    ledger = adopt_revert.read(cfg)
    assert len(ledger.snapshots) == 1, [entry.file for entry in ledger.snapshots]
    assert ledger.snapshots[0].original == ("User Genre",)
    assert ledger.snapshots[0].written_by("e1") and ledger.snapshots[0].written_by("e2")


def test_an_identifier_from_NEITHER_scheme_is_refused_by_the_reader(cfg):
    """``file`` was accepted as any non-empty string, so nothing pinned its shape."""
    for identifier in ("not-a-digest", "a" * 23, "a" * 25, "dev-ino:1", ""):
        adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
        adopt_revert.path_for(cfg).write_text(json.dumps(_one_record_document(file=identifier)))
        with pytest.raises(adopt_revert.RevertLedgerUnreadable):
            adopt_revert.read(cfg)

    # And both shapes this build can legitimately have written are read.
    for identifier in ("a" * 24, "dev-ino:16777232:12345"):
        adopt_revert.path_for(cfg).write_text(json.dumps(_one_record_document(file=identifier)))
        assert adopt_revert.read(cfg).snapshots[0].file == identifier


def test_a_reverted_file_that_has_since_been_deleted_is_reported_not_silent(cfg, tmp_path):
    """And it is reported AS DELETED, which is the half the key alone cannot say."""
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
    """The tag writer returns False rather than raising, so the return must be read."""
    path = _synth(tmp_path, ".flac")
    _adopt(cfg, path, written="New")
    report = adopt_revert.revert_tags(cfg, restore=lambda *_: False)
    assert report.restored == ()
    assert list(report.failed) == [(str(path), "genre")]
    assert report.failed[(str(path), "genre")] == "the container refused the write"


#: EVERY container the writer claims, derived from the writer's own table rather than listed beside
#: it.
LEDGER_CONTAINERS = sorted(tags._DIALECT_BY_SUFFIX)

#: Every shape of "what the file held" that an exact reader has to preserve.
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

#: Fields driven through the exact pair, one per dialect SHAPE rather than one per name.
LEDGER_FIELDS = ["genre", "title", "energylevel"]


@pytest.mark.parametrize("suffix", LEDGER_CONTAINERS)
@pytest.mark.parametrize("original", LOSSY_SHAPES)
def test_the_ledger_records_what_the_file_ACTUALLY_HELD(cfg, tmp_path, suffix, original):
    """The ledger is the whole safety net for a write no snapshot covers."""
    path = _synth(tmp_path, suffix)
    if original is not None:
        assert tags.write_tag_values(path, "genre", original) is True

    expected = _expected_after_writing(original, suffix, "genre")
    assert _oracle_values(path, "genre") == expected, (
        "the fixture did not put on disk what this test believes it did"
    )

    # THROUGH THE COMPOSED CALL, which is the shape ``apply_plan`` uses and the only one
    # that stamps.
    assert _adopt(cfg, path, written="Adopted")[1] is True
    recorded = adopt_revert.read(cfg).snapshots[0]
    assert recorded.original == expected, (
        f"the ledger recorded {recorded.original!r} for a file the container "
        f"itself says holds {expected!r}"
    )
    assert recorded.digest_state is adopt_revert.DigestState.RECORDED

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}
    assert _oracle_values(path, "genre") == expected, "the restore was not exact"


#: The one shape a container genuinely cannot hold, stated rather than tolerated. mutagen drops an
#: ID3 text frame whose only value is the empty string, so the field really IS absent afterwards
#: and an exact reader has to say so.
def _drops_the_empty_string(suffix: str, field: str) -> bool:
    # Measured across every frame shape rather than assumed: a TXXX frame drops an empty
    # value exactly as a plain text frame does, so the rule is the DIALECT and nothing
    # finer.
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
    """What the container holds, read WITHOUT the reader under test."""
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
def test_the_exact_reader_agrees_with_the_container_itself(tmp_path, suffix, original, field):
    """The reader against an oracle, with no ledger in the way."""
    path = _synth(tmp_path, suffix)
    if original is not None:
        assert tags.write_tag_values(path, field, original) is True
    expected = _expected_after_writing(original, suffix, field)
    assert _oracle_values(path, field) == expected
    assert tags.read_tag_values(path, field) == expected


def test_the_container_list_is_the_writers_own(tmp_path):
    """Both lists, against each other, so neither can drift alone (P3)."""
    assert set(LEDGER_CONTAINERS) == set(tags._DIALECT_BY_SUFFIX)
    assert len(LEDGER_CONTAINERS) == len(tags._DIALECT_BY_SUFFIX)
    assert {tags.dialect_of(s) for s in LEDGER_CONTAINERS} == set(tags.Dialect), (
        "a whole tag dialect has no container in the list that drives it"
    )
    for suffix in LEDGER_CONTAINERS:
        assert _synth_in(tmp_path / suffix[1:], suffix).exists()


@pytest.mark.parametrize("suffix", LEDGER_CONTAINERS)
def test_an_mp3s_legacy_id3v1_genre_survives_a_write_and_a_revert(cfg, tmp_path, suffix):
    """mutagen rewrites a PRESENT ID3v1 tag from the v2 frames on every save."""
    from tests.test_tags import _decoded_md5

    path = _synth(tmp_path, suffix)
    tags.write_genre(path, "Original Genre")
    before_audio = _decoded_md5(path)
    trailer_before = _id3v1_of(path)
    if suffix == ".mp3":
        trailer_before = _give_it_an_id3v1_genre(path, 31)
        assert trailer_before is not None and trailer_before[-1] == 31

    assert _adopt(cfg, path, written="Adopted")[1] is True
    assert _id3v1_of(path) == trailer_before, "the write destroyed the legacy tag"

    adopt_revert.revert_tags(cfg)
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert _id3v1_of(path) == trailer_before, "the revert destroyed the legacy tag"
    assert _decoded_md5(path) == before_audio, "preserving the legacy tag moved an audio byte"


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
    """Absence of a fact and absence AS a fact are not the same fact."""
    document = {
        "schema_version": adopt_revert.SCHEMA_VERSION,
        "snapshots": [{"file": "f", "field": "genre", "path": "/x/y.flac", "written": "Adopted"}],
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
    """:func:`_one_record_document` with the ``digest_state`` KEY REMOVED."""
    document = _one_record_document(**overrides)
    del document["snapshots"][0]["digest_state"]
    return document


#: Every JSON shape Python calls false, plus the two it calls true.
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
    """Truthiness is not a type check, and six shapes went through it silently."""
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(json.dumps(_document_with_no_state(digest=digest)))
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def test_null_and_absent_are_both_NO_DIGEST_and_neither_is_an_acceptance(cfg):
    """The three shapes that legitimately mean "nothing was written down here"."""
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


def test_a_digest_state_of_NULL_is_not_the_same_document_as_no_key_at_all(cfg, tmp_path):
    """Absence of a fact and absence AS a fact, in the field that used to collapse them."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
    assert adopt_revert.read(cfg).snapshots[0].digest_state is adopt_revert.DigestState.ABSENT


def test_a_state_that_DISOWNS_a_digest_it_is_holding_is_refused_too(cfg, tmp_path):
    """The contradiction check, in the direction that was never checked."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    assert document["snapshots"][0]["digest"] == hashlib.sha256(path.read_bytes()).hexdigest()

    for disowning in ("absent", "unreadable"):
        document["snapshots"][0]["digest_state"] = disowning
        adopt_revert.path_for(cfg).write_text(json.dumps(document))
        with pytest.raises(adopt_revert.RevertLedgerUnreadable) as refused:
            adopt_revert.read(cfg)
        assert "carries one anyway" in str(refused.value), str(refused.value)


def test_a_document_written_BEFORE_the_state_existed_still_spends_its_digest(cfg, tmp_path):
    """Back compatibility, in the direction that matters: it must still ACCEPT."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    del document["snapshots"][0]["digest_state"]
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    record = adopt_revert.read(cfg).snapshots[0]
    assert record.digest and record.digest_state is adopt_revert.DigestState.RECORDED

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_record_claiming_a_digest_it_does_not_carry_is_refused(cfg):
    """A state and a digest that contradict each other cannot both be believed."""
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(_one_record_document(digest="", digest_state="recorded"))
    )
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def test_a_digest_state_this_build_does_not_know_is_refused(cfg):
    """Positive recognition, like every other field in this reader."""
    adopt_revert.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    adopt_revert.path_for(cfg).write_text(
        json.dumps(_one_record_document(digest_state="probably-fine"))
    )
    with pytest.raises(adopt_revert.RevertLedgerUnreadable):
        adopt_revert.read(cfg)


def test_a_file_replaced_since_adoption_wrote_it_is_refused_not_overwritten(cfg, tmp_path):
    """The record named a path and nothing else, so it described any bytes there."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")
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
    """The one legitimate library this guard cannot recognize, held to explicitly."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted Genre", entry_id="e1")
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
    """A backup restore, an rsync without timestamps, a cloud re-download."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted Genre", entry_id="e1")
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
    """The modification time is metadata, and metadata is not the bytes."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
        "size and time were forged and the recorded digest was never asked"
    )
    assert list(report.failed) == [key]
    assert tags.read_genre_from_file(path) == "Stranger Genre"
    assert adopt_revert.read(cfg).snapshots != (), "the record was dropped anyway"


def test_a_file_of_a_DIFFERENT_SIZE_is_refused_without_reading_it(cfg, tmp_path):
    """Different sizes cannot be the same bytes, so the digest is not asked."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    record = adopt_revert.read(cfg).snapshots[0]
    path.write_bytes(path.read_bytes() + b"\x00" * 4096)
    assert path.stat().st_size != record.size

    reads: list[Path] = []
    real_digest = adopt_revert.digest_of
    adopt_changed.digest_of = lambda p: (reads.append(p), real_digest(p))[1]
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        adopt_changed.digest_of = real_digest

    assert list(report.failed) == [(str(path), "genre")]
    assert reads == [], f"a whole file was hashed to confirm what stat said: {reads}"
    # THE LITERAL, not the constant the message is built from.
    assert (
        "its bytes are not the ones this record was stamped from, and nothing "
        "here can say whether another program wrote them or this tool did"
        in report.failed[(str(path), "genre")]
    )


def test_a_digest_recorded_with_no_size_is_still_compared_rather_than_refused(cfg, tmp_path):
    """The size shortcut is a shortcut, so its absence must not become a verdict."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    document = json.loads(adopt_revert.path_for(cfg).read_text())
    document["snapshots"][0]["size"] = None
    adopt_revert.path_for(cfg).write_text(json.dumps(document))
    stripped = adopt_revert.read(cfg).snapshots[0]
    assert stripped.size is None and stripped.digest

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_file_that_cannot_be_READ_is_not_reported_as_somebody_elses_bytes(cfg, tmp_path):
    """An input output error is not a verdict about the file's content."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    key = (str(path), "genre")
    with pytest.MonkeyPatch.context() as unreadable:
        unreadable.setattr(adopt_changed, "digest_of", lambda _p: "")
        report = adopt_revert.revert_tags(cfg)
    assert list(report.failed) == [key]
    assert "its bytes cannot be read here to compare" in report.failed[key], report.failed[key]
    assert "not the ones adoption left" not in report.failed[key]
    assert adopt_revert.read(cfg).snapshots != ()

    # And it is still spendable once the person says the file is theirs.
    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_a_READ_ONLY_file_and_directory_are_the_writers_problem_not_the_guards(cfg, tmp_path):
    """The guard reads, so a mode that blocks WRITING must not become a refusal."""
    quiet = tmp_path / "readonly-dir"
    quiet.mkdir()
    path = _synth_in(quiet, ".flac")
    locked = _synth_in(tmp_path / "locked", ".flac")
    for target in (path, locked):
        tags.write_genre(target, "Original Genre")
        _adopt(cfg, target, written="Adopted", entry_id="e1")

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
    """The guard stats and reads ``record.path``, so the path has to still resolve."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
    """The legitimate case the digest check must not cost, held to explicitly."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    record = adopt_revert.read(cfg).snapshots[0]
    assert record.digest, "an unstamped record would pass this without the check"

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert report.restored == ((str(path), "genre"),)
    assert tags.read_genre_from_file(path) == "Original Genre"
    assert adopt_revert.read(cfg).snapshots == ()


def test_an_UNSTAMPED_record_refuses_a_file_that_was_replaced(cfg, tmp_path):
    """The widest door in the guard, and an ordinary interrupt is the key to it."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    # THE INTERRUPT: the record half lands, the tag write never does.
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="Adopted", entry_id="e1")
    record = adopt_revert.read(cfg).snapshots[0]
    assert (record.size, record.mtime_ns, record.digest) == (None, None, "")
    assert record.digest_state is adopt_revert.DigestState.ABSENT

    # MONTHS LATER: a different recording at the same path.
    stranger = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(stranger, {"genre": "Stranger Genre", "title": "Somebody Else"})
    path.write_bytes(stranger.read_bytes())
    assert tags.read_genre_from_file(path) == "Stranger Genre", (
        "the fixture did not put a different recording at the path"
    )

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (), (
        "an unstamped record accepted a file it has no evidence about at all"
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
    """The other direction, which is what makes the refusal safe to add."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="Adopted", entry_id="e1")
    tags.write_genre(path, "Adopted")  # the write that landed before the crash
    key = (str(path), "genre")

    assert list(adopt_revert.revert_tags(cfg).failed) == [key]
    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed
    assert tags.read_genre_from_file(path) == "Original A"
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_stamping_read_that_FAILS_is_recorded_as_its_own_state(cfg, tmp_path):
    """ "The digest could not be computed" and "no digest exists" are two facts."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    with pytest.MonkeyPatch.context() as unreadable:
        unreadable.setattr(adopt_changed, "digest_of", lambda _p: "")
        record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")
    assert landed

    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.digest == ""
    assert record.size is not None and record.mtime_ns is not None
    stored = json.loads(adopt_revert.path_for(cfg).read_text())["snapshots"][0]
    assert stored["digest_state"] == "unreadable", (
        "the failed read is not distinguishable on disk from a record that never had a digest"
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
        "a record whose stamping read failed accepted a forged size and time"
    )
    assert (
        "adoption could not read back what it had just written, so the bytes it "
        "left were never recorded"
    ) in report.failed[key], report.failed[key]
    assert tags.read_genre_from_file(path) == "Stranger Genre"

    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,), forced.failed


def test_the_stamping_read_is_RETRIED_before_the_record_gives_up(cfg, tmp_path):
    """A transient failure must not cost a record its only evidence."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    attempts = {"n": 0}
    real_digest = adopt_revert.digest_of

    def fails_once(target):
        attempts["n"] += 1
        return "" if attempts["n"] == 1 else real_digest(target)

    adopt_changed.digest_of = fails_once
    try:
        record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")
    finally:
        adopt_changed.digest_of = real_digest

    assert landed and attempts["n"] == 2, attempts
    assert record.digest_state is adopt_revert.DigestState.RECORDED
    assert record.digest == hashlib.sha256(path.read_bytes()).hexdigest()
    # And the record it saved is spendable with no override.
    assert adopt_revert.revert_tags(cfg).failed == {}
    assert tags.read_genre_from_file(path) == "Original A"


def test_a_stamping_STAT_that_fails_records_the_state_rather_than_asserting_it_cannot(
    cfg, tmp_path
):
    """The branch that carried ``pragma: no cover`` on a claim that does not follow."""
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
        record, landed = _adopt(
            cfg, path, written="Adopted", entry_id="e1", write_field=write_then_break
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


def test_a_record_with_no_digest_refuses_INSTEAD_OF_falling_back_to_the_metadata(cfg, tmp_path):
    """The fallback that let round 3's forgery straight back in one layer down."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
    assert forged.restored == (), "a record with no digest accepted a file on size and time alone"
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


def test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway(cfg, tmp_path):
    """The shortcut that skipped the only unforgeable evidence to save nothing."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
        evicted.setattr(adopt_changed, "digest_of", lambda p: (reads.append(p), real_digest(p))[1])
        evicted.setattr(Path, "stat", evicted_stat)

        # THE REAL WRITER, which is the whole difference from the version this
        # replaces: the restore below opens the file with mutagen and rewrites it.
        report = adopt_revert.revert_tags(cfg)

    assert report.failed == {}, report.failed
    assert report.restored == ((str(path), "genre"),)
    # TWO READS, AND THE COUNT IS THE COST WRITTEN DOWN RATHER THAN ROUNDED OFF.
    assert reads == [path, path], (
        f"the evicted file was decided about without asking the one piece of "
        f"evidence a replacement cannot forge, reads={reads}"
    )
    assert tags.read_genre_from_file(path) == "Original Genre", (
        "the accepting path did not rewrite the file"
    )


def _legacy_ledger(cfg_value, *records) -> None:
    """Write a ledger keyed by the PREVIOUS path-digest scheme, verbatim."""
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
        json.dumps({"schema_version": adopt_revert.SCHEMA_VERSION, "snapshots": snapshots})
    )


#: One revert pass, in a real interpreter, reporting as JSON.
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
    """The shape that destroyed the value, driven end to end on the ledger on disk."""
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


def test_a_REWRITE_INSIDE_ONE_TICK_that_moves_no_stat_field_is_still_caught(cfg, tmp_path):
    """The window a metadata-decided acceptance left in front of the byte-decided one."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
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
        swapping.setattr(adopt_changed, "digest_of", swap_the_bytes_after_the_first_read)
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
        "the restore ran on bytes this pass had never read"
    )
    # AND THE REFUSAL IS PINNED IN FULL, wrapper and reason together.
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
    """Ambiguity is a property of the DOCUMENT, so it cannot be filtered away."""
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
    # THE WHOLE MESSAGE, wrapper and reason, spelled out rather than sampled.
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
    # AND IT NAMES NO COMMAND, because `crate doctor` is not a verb this build has: the
    # registry marks it planned_in="U27" and the parser answers `invalid choice:
    # 'doctor'`.
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
        "a record was dropped, so the original it held is now in no file and no ledger"
    )


def test_a_SINGLE_RECORD_group_is_never_refused_as_ambiguous(cfg, tmp_path):
    """The over-tightened direction, which refusing on the SCHEME would produce."""
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
    _adopt(cfg, fresh, written="Adopted Bucket", entry_id="e1")
    assert len(adopt_revert.read(cfg).snapshots) == 2

    report = adopt_revert.revert_tags(cfg)
    assert report.failed == {}, report.failed
    assert tags.read_genre_from_file(legacy_path) == "Legacy Genre"
    assert tags.read_genre_from_file(fresh) == "Fresh Genre"


def test_ONE_FORCE_ENTRY_overrides_EXACTLY_ONE_RECORD(cfg, tmp_path):
    """A force key reaches the record it names and never the one beside it."""
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


def test_a_FORCE_KEY_that_names_two_UNIDENTIFIABLE_records_overrides_neither(cfg, tmp_path):
    """The residue after the ghost rule, and the one place the count guard decides."""
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


def test_a_FIFO_at_the_recorded_path_refuses_instead_of_blocking_forever(cfg, tmp_path):
    """The hang, and it held the lock that serializes every write in the library."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
    assert ("what is at that path is not a regular file, so it has no bytes to compare") in only, (
        only
    )


def test_a_DIRECTORY_at_the_recorded_path_refuses_as_ITS_OWN_reason(cfg, tmp_path):
    """ "that is not a file" and "its bytes cannot be read" are different facts."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
    path.unlink()
    path.mkdir()

    key = (str(path), "genre")
    report = adopt_revert.revert_tags(cfg)
    assert (
        "what is at that path is not a regular file, so it has no bytes to compare"
    ) in report.failed[key], report.failed[key]
    assert "cannot be read here to compare" not in report.failed[key]


def test_a_read_that_RUNS_OUT_OF_TIME_is_not_reported_as_unreadable(cfg, tmp_path):
    """``TimeoutError`` IS an ``OSError``, so a bound folded into "unreadable"."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")

    def never_arrives(target, **_kwargs):
        raise TimeoutError(f"{target} is still being fetched")

    key = (str(path), "genre")
    real = adopt_revert.digest_of
    adopt_changed.digest_of = never_arrives
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        adopt_changed.digest_of = real

    assert report.restored == ()
    assert (
        "its bytes did not finish arriving within the time this pass waits, "
        "which is what a file still being fetched from a provider looks like"
    ) in report.failed[key], report.failed[key]
    assert "cannot be read here to compare" not in report.failed[key]


def test_the_deadline_ends_a_read_that_keeps_arriving_forever(tmp_path):
    """The bound itself, on the function that owns it."""
    endless = tmp_path / "endless.bin"
    endless.write_bytes(b"\x00" * 8)

    class _TrickleThenStop:
        """A stream that arrives too slowly, and then ENDS."""

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
    # Counted in blocks rather than timed, R-759.
    read = 100 - stream.blocks
    assert read <= 20, (
        f"the deadline is asked between blocks, so the read must end near it "
        f"rather than run the stream on; {read} of 100 blocks were read"
    )


def test_the_stamping_read_is_asked_EXACTLY_TWICE_and_not_three_times(cfg, tmp_path):
    """Pinned from BOTH sides, which is what the docstring's argument requires."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    attempts = {"n": 0}

    def always_fails(_target, **_kwargs):
        attempts["n"] += 1
        return ""

    real = adopt_revert.digest_of
    adopt_changed.digest_of = always_fails
    try:
        record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")
    finally:
        adopt_changed.digest_of = real

    assert landed
    assert attempts["n"] == 2, attempts
    assert record.digest_state is adopt_revert.DigestState.UNREADABLE


def test_a_stamping_read_that_TIMES_OUT_is_not_retried_at_all(cfg, tmp_path):
    """A retry is cheap for a transient error and is the whole deadline again here."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")

    attempts = {"n": 0}

    def times_out(target, **_kwargs):
        attempts["n"] += 1
        raise TimeoutError(f"{target} is still being fetched")

    real = adopt_revert.digest_of
    adopt_changed.digest_of = times_out
    try:
        record, landed = _adopt(cfg, path, written="Adopted", entry_id="e1")
    finally:
        adopt_changed.digest_of = real

    assert landed and attempts["n"] == 1, attempts
    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.digest == ""


def test_a_failed_stamping_STAT_does_not_leave_a_digest_it_has_disowned(cfg, tmp_path):
    """A record this build wrote could make its own ledger unreadable."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
        record, _landed = _adopt(
            cfg, path, written="Adopted", entry_id="e2", write_field=write_then_break
        )
    finally:
        Path.stat = real_stat

    assert record.digest_state is adopt_revert.DigestState.UNREADABLE
    assert record.digest == "" and record.size is None and record.mtime_ns is None
    # The document this build just wrote is readable, which is the finding.
    assert adopt_revert.read(cfg).snapshots[0].digest == ""


def test_the_FETCH_happens_before_the_lock_and_the_DECIDING_read_happens_under_it(cfg, tmp_path):
    """Two reads, and which of them is allowed to decide anything."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="Adopted", entry_id="e1")

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

    adopt_changed.digest_of = note_the_lock
    try:
        report = adopt_revert.revert_tags(cfg)
    finally:
        adopt_changed.digest_of = real

    assert report.failed == {}, report.failed
    assert held_during_read == [False, True], (
        "the two reads are the prefetch and the guard's own, in that order"
    )
    assert tags.read_genre_from_file(path) == "Original Genre"


def test_bytes_THIS_PASS_ITSELF_replaced_are_never_accepted_on(cfg, tmp_path):
    """The pass must not accept a record on bytes its own earlier restore destroyed."""
    path = _synth(tmp_path, ".flac")
    tags.write_tags(path, {"genre": "User Genre", "title": "User Title"})
    # TITLE FIRST, GENRE SECOND, so the record visited first is the one whose
    # digest is current and whose restore therefore lands.
    adopt_revert.write_tag_with_record(
        cfg, path, field="title", written="Adopted Title", entry_id="e1"
    )
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
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
        "a record was accepted on a digest of the bytes this same pass had already replaced"
    )
    assert tags.read_genre_from_file(path) == "User Genre"
    assert tags.read_tag(path, "title") == "Adopted Title"


def test_the_refusal_says_the_cause_is_UNKNOWN_and_that_leaving_it_is_safe(cfg, tmp_path):
    """The message told a person their file had been replaced, and then armed them."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "User Genre")
    _adopt(cfg, path, written="Adopted Bucket", entry_id="e1")
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
    """The constant the two eviction fixtures used to be checked against."""
    assert adopt_scan.DATALESS_FLAG == 0x40000000


def test_an_interrupted_revert_pass_can_be_retried(cfg, tmp_path):
    """A pass restores a file and dies before the ledger is rewritten."""
    originals = {
        _synth_in(tmp_path / "one", ".flac"): "Original One",
        _synth_in(tmp_path / "two", ".flac"): "Original Two",
    }
    for path, genre in originals.items():
        tags.write_genre(path, genre)
        _adopt(cfg, path, written="Adopted Genre", entry_id="e1")
    assert len(adopt_revert.read(cfg).snapshots) == 2

    class _Died(RuntimeError):
        pass

    # WHICHEVER RECORD THE PASS REACHES FIRST, because the ledger sorts by the file's
    # digest and not by the order the records were made.
    seen: list[Path] = []

    def restore_then_die(target, field, original):
        seen.append(target)
        if len(seen) > 1:
            raise _Died("the pass died after one file and before the ledger write")
        return adopt_revert.restore_tag(target, field, original)

    with pytest.raises(_Died):
        adopt_revert.revert_tags(cfg, restore=restore_then_die)
    assert tags.read_genre_from_file(seen[0]) == originals[seen[0]]
    # THE RECORD IT FINISHED IS ALREADY GONE, which is what makes the retry possible.
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


def test_a_pass_that_dies_BEFORE_THE_LEDGER_WRITE_still_strands_that_one_record(cfg, tmp_path):
    """The window the per-record settle NARROWED rather than closed."""
    paths = {
        _synth_in(tmp_path / "one", ".flac"): "Original One",
        _synth_in(tmp_path / "two", ".flac"): "Original Two",
    }
    for path, genre in paths.items():
        tags.write_genre(path, genre)
        _adopt(cfg, path, written="Adopted", entry_id="e1")

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
    assert key in {(record.path, record.field) for record in adopt_revert.read(cfg).snapshots}, (
        "the record for the restored file was dropped, so there is no window at all"
    )

    retry = adopt_revert.revert_tags(cfg)
    assert list(retry.failed) == [key], "the window is closed rather than narrowed"
    assert tags.read_genre_from_file(done) == paths[done]

    # BOUNDED: the override writes the same original onto a file already holding
    # it, so the cost of the residue is one override and never a wrong value.
    cleared = adopt_revert.revert_tags(cfg, force=[key])
    assert cleared.restored == (key,)
    assert tags.read_genre_from_file(done) == paths[done]
    assert adopt_revert.read(cfg).snapshots == ()


def test_a_death_INSIDE_the_rewrite_is_a_different_window_and_a_weaker_bound(cfg, tmp_path):
    """The interrupted-pass bound covers the window AFTER the restore, not the one inside it."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _adopt(cfg, path, written="Adopted", entry_id="e1")
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
        # THE FIRST ONE IS THE CASE THE GUARD IS ACTUALLY FOR, and the round 2 version
        # of this test used only the second.
        "THE BUCKET ADOPTION WROTE",
        "Different B",
    ],
    ids=["stranger-shares-the-bucket", "stranger-has-its-own-genre"],
)
def test_a_genuinely_replaced_file_is_still_refused_and_force_gets_through(
    cfg, declared, tmp_path, stranger_genre
):
    """The guard still bites, and it is evidence rather than permission (P7)."""
    routable, _genre = _bucket_and_genre(declared)
    written = declared.bucket(routable).display
    if stranger_genre == "THE BUCKET ADOPTION WROTE":
        stranger_genre = written

    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    _adopt(cfg, path, written=written, entry_id="e1")
    # A DIFFERENT RECORDING at the same path. Different bytes, so this is not the
    # backup-restore case; the size differs too, which is the ordinary shape.
    replacement = _synth_in(tmp_path / "other", ".flac")
    tags.write_tags(replacement, {"genre": stranger_genre, "title": "Somebody Else"})
    path.write_bytes(replacement.read_bytes())

    key = (str(path), "genre")
    refused = adopt_revert.revert_tags(cfg)
    assert refused.restored == (), "the revert put one file's tag onto another file's audio"
    assert list(refused.failed) == [key]
    assert repr(key) in refused.failed[key], (
        "the refusal does not name the record it can be overridden for"
    )
    assert tags.read_genre_from_file(path) == stranger_genre
    assert adopt_revert.read(cfg).snapshots != (), "the record was dropped anyway"

    forced = adopt_revert.revert_tags(cfg, force=[key])
    assert forced.restored == (key,)
    assert tags.read_genre_from_file(path) == "Original A"
    assert adopt_revert.read(cfg).snapshots == ()


def test_force_overrides_the_record_it_names_and_no_other(cfg, tmp_path):
    """A per-record message must not hand out a pass-wide override."""
    mine = _synth_in(tmp_path / "mine", ".flac")
    stranger = _synth_in(tmp_path / "stranger", ".flac")
    for path, genre in ((mine, "Original Mine"), (stranger, "Original Stranger")):
        tags.write_genre(path, genre)
        _adopt(cfg, path, written="Adopted", entry_id="one_entry")
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
    """The per-track rule U19 paid for, applied to the undo log."""
    good = [_synth_in(tmp_path / f"g{i}", ".flac") for i in range(2)]
    for index, path in enumerate(good):
        tags.write_genre(path, f"Original {index}")
        _adopt(cfg, path, written="Adopted", entry_id="e1")

    # A THIRD FILE, so the bad record's own guard is satisfied and the pass truly
    # reaches the writer with an unknown field.
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
        "one record naming a field this build cannot write ended the pass"
    )
    assert list(report.failed) == [(str(odd), "bpm")]
    for index, path in enumerate(good):
        assert tags.read_genre_from_file(path) == f"Original {index}"
    assert len(adopt_revert.read(cfg).snapshots) == 1, (
        "the two records that were spent are still in the ledger"
    )


def test_the_value_adoption_WROTE_is_never_treated_as_the_files_identity(cfg, declared, tmp_path):
    """A bucket display name is shared by most of the library it was written to."""
    routable, _genre = _bucket_and_genre(declared)
    written = declared.bucket(routable).display
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original A")
    record, landed = _adopt(cfg, path, written=written, entry_id="e1")
    assert landed
    info = path.stat()
    assert record.digest == hashlib.sha256(path.read_bytes()).hexdigest(), (
        "the record does not carry the bytes adoption left"
    )
    assert (record.size, record.mtime_ns) == (info.st_size, info.st_mtime_ns)
    assert record.written == written
    assert tags.read_genre_from_file(path) == written
    # AND THE INODE IS NOT RECORDED, deliberately.
    stored = json.loads(adopt_revert.path_for(cfg).read_text())["snapshots"][0]
    assert "ino" not in stored and "dev" not in stored


def test_a_targeted_revert_answers_for_the_entry_that_actually_wrote(cfg, tmp_path):
    """First-write-wins means the SECOND adoption writes through the FIRST record."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")
    _adopt(cfg, path, written="First", entry_id="ap_one")
    _adopt(cfg, path, written="Second", entry_id="ap_two")
    assert tags.read_genre_from_file(path) == "Second"
    records = adopt_revert.read(cfg).snapshots
    assert len(records) == 1
    assert records[0].entry_id == "ap_one", "the second write replaced the original"
    assert records[0].original == ("Original Genre",)

    report = adopt_revert.revert_tags(cfg, entry_id="ap_two")
    assert report.restored == ((str(path), "genre"),), (
        "the revert reported success for work it did not do"
    )
    assert tags.read_genre_from_file(path) == "Original Genre"

    nothing = adopt_revert.revert_tags(cfg, entry_id="ap_never_wrote_anything")
    assert nothing.restored == () and nothing.failed == {}


def test_two_failed_fields_on_one_file_are_two_reasons(cfg, tmp_path):
    """The report was keyed on the path, so one file could only carry one reason."""
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
    """``clear_tags`` is the undo ``write_tags`` cannot express. Same classification."""
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


# The two readers: a wrong document is never an empty one


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
    """An empty ledger re-applies an approved plan from its first entry."""
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


@pytest.mark.parametrize("document", WRONG_REVERT_DOCUMENTS, ids=range(len(WRONG_REVERT_DOCUMENTS)))
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
    """The property the module docstring calls load bearing, asserted directly."""
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
    assert kept.snapshots[0].original == ("User Genre",), "the second record replaced the first"
    # And the one way a record IS legitimately amended still replaces it, which
    # is what keeps this from being fixable by refusing both.
    amended = kept.replacing(second)
    assert amended.snapshots[0].original == ("Adopted Bucket",)


def test_an_original_key_that_is_ABSENT_is_refused_rather_than_read_as_null(cfg):
    """Absence of a fact and absence AS a fact, in the field that owns the phrase."""
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


# The lock, proved by real processes


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
    """The shape this repository has shipped twice, refused a third time."""
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
    """The window that was one instruction wide and cost the only copy."""
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
        "the apply wrote its value with no record behind it"
    )
    remaining = adopt_revert.read(cfg).snapshots
    assert all(record.original == ("Original Genre",) for record in remaining), (
        "a surviving record no longer describes the value the file started with"
    )


def test_the_apply_loop_records_and_writes_through_the_ONE_locked_call():
    """The proof above is about the composed call; this is what carries it to apply."""
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
        "the apply loop composes the record and the write itself"
    )
    assert "snapshot_before_write" not in reached, "the apply loop takes the record half on its own"


def test_both_documents_and_their_lock_are_declared_state_entries():
    """A path composed under a state root is a file nothing walks or backs up."""
    for key in ("adoption_ledger", "adoption_tag_revert_log", "adoption_locks"):
        assert config.state_file(key) is not None


def test_the_applied_ledger_rolls_back_with_the_database(cfg):
    """COUPLED: every record it holds names a membership row a restore removes."""
    assert config.state_file("adoption_ledger").snapshot is config.SnapshotRole.COUPLED
    assert adopt_apply.path_for(cfg).parent == config.library_coupled_dir(cfg)


def test_the_revert_ledger_and_the_locks_never_roll_back(cfg):
    """The undo log argument, and the inode argument, one assertion each."""
    assert (
        config.state_file("adoption_tag_revert_log").snapshot is config.SnapshotRole.NEVER_RESTORED
    )
    assert config.state_file("adoption_locks").snapshot is config.SnapshotRole.NEVER_RESTORED
    assert adopt_revert.lock_path(cfg).parent == config.state_path("adoption_locks", cfg)
    assert config.library_coupled_dir(cfg) not in adopt_revert.lock_path(cfg).parents


# R19, and the structured output


# The registry: a marker that can expire, and an obligation somebody owns


def test_the_planned_marker_on_the_apply_verb_CAN_ACTUALLY_FIRE():
    """The countdown could never fire, in this build or in any future one."""
    import importlib.util  # noqa: PLC0415

    from cratekit.cli import registry  # noqa: PLC0415

    scan_entry = registry.entry("adopt.scan")
    apply_entry = registry.entry("adopt.apply")
    assert scan_entry.module.startswith("cratekit.adopt.")
    assert apply_entry.module.startswith("cratekit.adopt.")
    assert scan_entry.module != apply_entry.module, (
        "one module string for two verbs means the marker test keys on a name they share"
    )

    # THE WHOLE DEFECT IN ONE LINE, and it is the same line either way: this call used
    # to RAISE, and the raise was caught and read as absence.
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
        "the profile toggle is a different namespace from the package and was never the thing that was wrong"
    )


def test_no_landed_adoption_verb_still_owes_the_file_the_board_reads():
    """P5. ``scripts/board.py`` reads ``tests/_pending.py`` and nothing else."""
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
            assert unit == entry.planned_in, "the marker and the register name two different units"


def test_the_adoption_shell_never_reaches_into_the_layer_above_it():
    """KTD23, at the one place in this package that wants to break it."""
    from tests.test_layering import import_direction_violations  # noqa: PLC0415

    problems: list[str] = []
    for path in sorted(ADOPT_ROOT.rglob("*.py")):
        module = "cratekit.adopt" if path.stem == "__init__" else f"cratekit.adopt.{path.stem}"
        problems += import_direction_violations(path.read_text(), module)
    assert not problems, problems

    # Named rather than merely ranked, because "no upward import" is satisfied by a
    # shell that imports nothing at all, and the trap here is specific: the ONE cli
    # module a shell is allowed to name is the output contract.
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
    """An identifier nobody can recompute from the record is one nobody can audit."""
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
    """The duplicate-key shape, asked of two enums instead of one literal."""
    dispositions = {str(member) for member in adopt_scan.Disposition}
    categories = {str(member) for member in adopt_scan.Readability}
    assert dispositions.isdisjoint(categories), sorted(dispositions & categories)
    assert len(adopt_plan.AdoptionPlan(tree=TREE_ID).counts()) == len(dispositions) + len(
        categories
    )
