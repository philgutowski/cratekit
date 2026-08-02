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
import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import approval as adopt_approval
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import revert as adopt_revert
from cratekit.adopt import scan as adopt_scan
from cratekit.core import config, review, tags, taxonomy
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

    So the block count is asked instead. A probe that read the first byte to find
    out whether it could would fetch the whole library from the provider, which
    is the opposite of a scan.
    """
    music = Path(cfg.library.root) / "Music"
    dataless = music / "Dataless.flac"
    dataless.write_bytes(b"audio")
    real_stat = Path.stat

    class _Stat:
        st_blocks = 0
        st_size = 4096
        st_mode = real_stat(dataless).st_mode

    monkeypatch.setattr(Path, "stat", lambda self, **_: _Stat())
    monkeypatch.setattr(
        Path, "open", lambda *args, **kwargs: pytest.fail("the probe opened the file")
    )
    assert adopt_scan.probe_readability(dataless) is adopt_scan.Readability.ONLINE_ONLY


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


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 5: a tag write is reverted EXACTLY
# ═══════════════════════════════════════════════════════════════════════════


def test_a_tag_write_is_reverted_exactly(cfg, tmp_path):
    """The value that was there before comes back, byte for byte."""
    path = _synth(tmp_path, ".flac")
    tags.write_genre(path, "Original Genre")

    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    tags.write_genre(path, "Adopted Genre")
    assert tags.read_genre_from_file(path) == "Adopted Genre"

    report = adopt_revert.revert_tags(cfg)
    assert report.restored == (str(path),)
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

    adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted Genre", entry_id="e1"
    )
    tags.write_genre(path, "Adopted Genre")
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
    assert recorded[0].original == "Original Genre"
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
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="Adopted Genre")
    tags.write_genre(path, "Adopted Genre")

    again = adopt_revert.snapshot_before_write(
        cfg, path, field="genre", written="Adopted Genre"
    )
    assert again.original == "Original Genre"
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

    adopt_revert.revert_tags(cfg)
    assert tags.read_tag(path, "genre") == "Original Genre"
    assert tags.read_tag(path, "title") == "Original Title"


def test_one_file_in_two_composition_forms_is_one_record(cfg, tmp_path):
    """The primitive U31 exists for, and the cost of not using it here.

    A ledger keyed on the raw string holds two records for one accented filename,
    so a revert restores one of them and reports both done.
    """
    assert COMPOSED != DECOMPOSED
    assert adopt_revert.file_id(f"/x/{COMPOSED}") == adopt_revert.file_id(f"/x/{DECOMPOSED}")


def test_a_reverted_file_that_has_since_been_deleted_is_reported_not_silent(cfg, tmp_path):
    path = _synth(tmp_path, ".flac")
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="New")
    path.unlink()
    report = adopt_revert.revert_tags(cfg)
    assert report.restored == ()
    assert list(report.failed) == [str(path)]
    assert adopt_revert.read(cfg).snapshots != (), (
        "the record was dropped for a file that was never restored"
    )


def test_a_container_that_refuses_the_write_is_a_failure_not_a_restore(cfg, tmp_path):
    """The tag writer returns False rather than raising, so the return must be read."""
    path = _synth(tmp_path, ".flac")
    adopt_revert.snapshot_before_write(cfg, path, field="genre", written="New")
    report = adopt_revert.revert_tags(cfg, restore=lambda *_: False)
    assert report.restored == ()
    assert list(report.failed) == [str(path)]


def test_the_clear_path_removes_a_field_without_touching_the_audio(tmp_path):
    """``clear_tags`` is the undo ``write_tags`` cannot express. Same classification."""
    from tests.test_tags import _decoded_md5

    path = _synth(tmp_path, ".flac")
    tags.write_tags(path, {"genre": "Original Genre", "title": "Kept Title"})
    before = _decoded_md5(path)

    assert tags.clear_tags(path, ["genre"]) is True
    assert tags.read_tag(path, "genre") is None
    assert tags.read_tag(path, "title") == "Kept Title"
    assert _decoded_md5(path) == before


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
                        "file": "f",
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
