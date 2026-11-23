"""U11: the review queue, the decision stores, and the split between them.

R12: every state a person adjudicates is a persisted, addressable review item,
never a hand edited file. The harder tests use a REAL second process, since only
a second process sees what reached the disk.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output
from cratekit.core import config, review
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests import _pending
from tests import _source_guards as _guards
from tests._source_guards import (
    calls_review,
    constructs_a_csv_writer,
    constructs_review,
    methods_on_review_construction,
    offers_into,
    package_modules,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


# Fixtures and helpers


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured, saved library; the environment is set too, as ``from_dict`` follows it (P2)."""
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
def store(cfg):
    with review.open_store(cfg) as opened:
        yield opened


def _child_env() -> dict[str, str]:
    """The inherited environment, so a child resolves the same temporary library."""
    return {**os.environ, "PYTHONPATH": str(SRC_ROOT)}


def _in_another_process(*argv: str) -> subprocess.CompletedProcess:
    """Run the real command line in a separate interpreter and wait for it."""
    return subprocess.run(
        [sys.executable, "-m", "cratekit.cli", *argv],
        env=_child_env(),
        capture_output=True,
        text=True,
    )


def _start_another_process(*argv: str) -> subprocess.Popen:
    """Start the real command line WITHOUT waiting, so two of them overlap."""
    return subprocess.Popen(
        [sys.executable, "-m", "cratekit.cli", *argv],
        env=_child_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _start_separate_processes(script: str, *, workers: int, arguments) -> list[subprocess.Popen]:
    """Start one short script in several REAL interpreters at once."""
    return [
        subprocess.Popen(
            [sys.executable, "-c", script, *(str(value) for value in arguments(worker))],
            env=_child_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for worker in range(workers)
    ]


def _all_succeed(running: list[subprocess.Popen]) -> None:
    for process in running:
        out, err = process.communicate()
        assert process.returncode == 0, err or out


def _drive(*argv: str) -> tuple[int, dict, str]:
    """Run the real dispatcher in process and return the parsed envelope."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    return code, json.loads(out.getvalue()), err.getvalue()


def _refused(*argv: str, reason: str) -> dict:
    """Drive the dispatcher and assert a precondition refusal for ``reason``."""
    code, envelope, _ = _drive(*argv)
    assert code == int(ExitCode.PRECONDITION), argv
    assert envelope["cause"]["reason"] == reason
    return envelope


def _offer_one(store, *, key: str = "a", **overrides):
    """One item in the version-match queue, with a stable identity."""
    fields = {
        "queue": review.Queue.VERSION_MATCH,
        "kind": "version-difference",
        "identity": {"source": "list-1", "row": key},
        "payload": {"wanted": f"track {key}", "found": f"track {key} (edit)"},
        "options": (
            review.Option(option_id="opt-accept", summary="the edit is the same recording"),
            review.Option(option_id="opt-other", summary="a different recording entirely"),
        ),
        "handler_key": "match.run",
    }
    fields.update(overrides)
    return review.offer(store, **fields)


def _offer_many(store, keys) -> list[str]:
    """One item per key, in order, skipping the per commit fsync for the population only."""
    store.conn.execute("PRAGMA synchronous=NORMAL")
    try:
        return [_offer_one(store, key=key).item_id for key in keys]
    finally:
        store.conn.execute("PRAGMA synchronous=FULL")


def _document(*items, exported: str = "2026-01-01T00:00:00+00:00") -> dict:
    """An export document carrying ``items``."""
    return {"export": review.EXPORT_VERSION, "queue": "", "exported": exported, "items": list(items)}


def _written(path: Path, *items) -> Path:
    path.write_text(json.dumps(_document(*items)))
    return path


def _stored_verdict(store, item_id: str):
    """The raw verdict column, past the reader's coercion."""
    row = store.conn.execute(
        "SELECT verdict FROM review_items WHERE item_id = ?", (item_id,)
    ).fetchone()
    return row["verdict"]


# Part 1: identity, and the storage that survives the process


def test_an_item_identifier_is_derived_from_stable_facts_rather_than_a_display_name():
    """D5. The identifier is a function of queue, kind and identity, and key order is not identity."""
    first = review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {"row": "7"})
    again = review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {"row": "7"})
    other = review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {"row": "8"})
    assert first == again
    assert first != other
    assert review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", {"a": "1", "b": "2"}
    ) == review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", {"b": "2", "a": "1"}
    )


def test_an_identity_with_nothing_in_it_is_refused():
    """An empty identity hashes to one value, so every item would collide."""
    with pytest.raises(CratekitError) as excinfo:
        review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", {})
    assert excinfo.value.cause.reason == "review-selection-invalid"


# The identity is NORMALIZED before hashing, so producers that mean one candidate agree.


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ({"track_id": 7}, {"track_id": "7"}),
        ({"track_id": 7.0}, {"track_id": "7"}),
        ({"flag": True}, {"flag": "true"}),
        ({"pair": [1, "2"]}, {"pair": ["1", 2]}),
        ({"nested": {"row": 3}}, {"nested": {"row": "3"}}),
    ],
)
def test_the_same_candidate_spelled_two_ways_is_one_identifier(left, right):
    """A type difference is not a different candidate, for items and suppressions alike."""
    assert review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", left
    ) == review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", right)
    assert review.suppression_id_for("declines", "removed-file", left) == (
        review.suppression_id_for("declines", "removed-file", right)
    )


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ({"track_id": None}, {"track_id": "None"}),
        ({"track_id": None}, {"track_id": ""}),
        ({"flag": True}, {"flag": 1}),
        ({"track_id": "7"}, {"track_id": " 7"}),
    ],
)
def test_normalizing_the_identity_does_not_collapse_facts_that_differ(left, right):
    """Absent and the text "None" are different facts; merging them settles an unmade decision."""
    assert review.item_id_for(
        review.Queue.VERSION_MATCH, "version-difference", left
    ) != review.item_id_for(review.Queue.VERSION_MATCH, "version-difference", right)


def test_the_same_candidate_under_two_spellings_of_one_kind_is_one_item(store):
    """A kind is an identifier and never a display name (D5, R19)."""
    first, again = (
        review.offer(
            store, queue=review.Queue.VERSION_MATCH, kind=kind,
            identity={"source": "list-1", "row": "a"}, payload={"wanted": "one"},
        )
        for kind in ("version-difference", "Version_Difference")
    )
    assert again.item_id == first.item_id
    assert again.kind == first.kind, (
        "the stored kind is normalized, or a predicate on one spelling matches nothing"
    )
    assert review.count_unresolved(store) == 1


def test_an_item_records_the_identity_it_was_addressed_by(store):
    """Stored, so a duplicate or a collision is detectable afterwards."""
    item = _offer_one(store)
    assert review.identity_of(store, item.item_id) == {"source": "list-1", "row": "a"}


def test_two_different_candidates_that_hash_alike_are_refused_rather_than_merged(
    store, monkeypatch
):
    """A collision, forced here, is never settled silently by the first one there."""
    monkeypatch.setattr(review, "item_id_for", lambda *args, **kwargs: "rv_forced")

    def offer(row):
        return review.offer(
            store, queue=review.Queue.VERSION_MATCH, kind="version-difference",
            identity={"source": "list-1", "row": row}, payload={},
        )

    offer("a")
    with pytest.raises(CratekitError) as excinfo:
        offer("b")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_the_queue_lives_where_the_state_inventory_says_and_is_owner_only(cfg, store):
    """P1: the file mode and the DIRECTORY mode, because one without the other is nothing."""
    declared = config.state_path("review_queue", cfg)
    assert review.queue_path(cfg).parent == declared
    assert review.queue_path(cfg).exists()
    if hasattr(os, "chmod"):
        assert declared.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE
        assert review.queue_path(cfg).stat().st_mode & 0o777 == config.PRIVATE_FILE_MODE


def test_every_file_the_queue_creates_is_owner_only_derived_by_walking(cfg, store):
    """P3: the set is DERIVED by walking, so the write-ahead log beside the database is covered."""
    _offer_one(store)
    root = config.state_path("review_queue", cfg)
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    for current, directories, files in os.walk(root):
        for name in directories:
            path = Path(current) / name
            assert path.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE, path
        for name in files:
            path = Path(current) / name
            assert path.stat().st_mode & 0o777 == config.PRIVATE_FILE_MODE, path


def test_an_offered_item_is_addressable_and_starts_unresolved(store):
    item = _offer_one(store)
    assert item.item_id
    assert item.verdict is None
    assert review.get(store, item.item_id) == item


def test_an_item_survives_the_handle_that_created_it(cfg, store):
    item = _offer_one(store)
    store.close()
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, item.item_id).payload == item.payload


def test_an_unknown_identifier_refuses_by_name_rather_than_returning_nothing(store):
    """Returning None would make a typo indistinguishable from an empty queue."""
    with pytest.raises(CratekitError) as excinfo:
        review.get(store, "rv_not_a_real_item")
    assert excinfo.value.cause.reason == "review-item-unknown"
    assert excinfo.value.cause.detail["item_id"] == "rv_not_a_real_item"


def test_offering_the_same_candidate_twice_produces_one_item(store):
    first = _offer_one(store)
    second = _offer_one(store)
    assert first.item_id == second.item_id
    assert len(review.list_items(store).items) == 1


def test_a_queue_nothing_declares_is_refused_and_the_refusal_names_the_declared_ones(store):
    with pytest.raises(CratekitError) as excinfo:
        _offer_one(store, queue="not-a-declared-queue")
    cause = excinfo.value.cause
    assert cause.reason == "review-queue-undeclared"
    assert "not-a-declared-queue" in cause.message


# Part 2: the split between an adjudication surface and a plain output


def test_every_declared_surface_says_which_side_of_the_split_it_is_on():
    """Approach step 4: outputs stay files. Asserted over the declaration, so a new surface is covered."""
    assert review.SURFACES
    for surface in review.SURFACES:
        assert surface.why, f"{surface.legacy_file} does not say why"
        if surface.adjudicated:
            assert surface.queue is not None, f"{surface.legacy_file} adjudicates nothing"
        else:
            assert surface.queue is None, (
                f"{surface.legacy_file} is a plain output; outputs stay files"
            )


def test_the_declared_queues_are_exactly_the_adjudicated_surfaces_queues():
    """Both directions: a queue with no surface, and a surface naming an undeclared queue."""
    declared = {str(surface.queue) for surface in review.SURFACES if surface.adjudicated}
    assert declared == set(review.adjudicated_queues())
    assert declared == {str(member) for member in review.Queue}


def test_several_legacy_files_may_fold_into_one_queue_and_that_is_the_point():
    """Several files may share one queue; one file may not have two."""
    files = [surface.legacy_file for surface in review.SURFACES if surface.legacy_file]
    assert len(files) == len(set(files))
    folded = [s.legacy_file for s in review.SURFACES if s.adjudicated and s.legacy_file]
    queues = {str(s.queue) for s in review.SURFACES if s.adjudicated and s.legacy_file}
    assert len(folded) > len(queues), (
        "no legacy file folds into a shared queue: a rename, not a consolidation"
    )


def test_a_plain_output_cannot_be_smuggled_into_the_queue(store):
    """The split has teeth only if the queue refuses the other side of it."""
    output = next(s for s in review.SURFACES if not s.adjudicated)
    with pytest.raises(CratekitError) as excinfo:
        _offer_one(store, queue=output.legacy_file)
    assert excinfo.value.cause.reason == "review-queue-undeclared"


# Part 3: a different process, which is the requirement R12 actually states


def test_an_item_resolved_in_one_process_is_seen_resolved_by_another(cfg, store):
    """The plan's first test scenario, run with a real interpreter on each side."""
    item = _offer_one(store)
    store.close()
    done = _in_another_process(
        "--output", "json", "review", "resolve", item.item_id, "--verdict", "accepted",
        "--option", "opt-accept",
    )
    assert done.returncode == 0, done.stderr
    envelope = json.loads(done.stdout)
    assert envelope["data"]["items"][0]["verdict"] == "accepted"
    with review.open_store(cfg) as reopened:
        settled = review.get(reopened, item.item_id)
    assert settled.verdict is review.Verdict.ACCEPTED
    assert settled.option == "opt-accept"
    assert settled.actor


# Part 4: a verdict persists, so the same decision is never re-asked


def test_re_offering_a_settled_item_does_not_reopen_it(store):
    """A producer meeting the same candidate again must not re-ask an answered question."""
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="tester")
    again = _offer_one(store)
    assert again.verdict is review.Verdict.ACCEPTED
    assert review.list_items(store).items == ()


def test_re_offering_an_open_item_refreshes_what_it_shows(store):
    """Still open, so the newest description of the candidate is the useful one."""
    item = _offer_one(store)
    refreshed = _offer_one(store, payload={"wanted": "track a", "found": "track a (2026 edit)"})
    assert refreshed.item_id == item.item_id
    assert refreshed.payload["found"] == "track a (2026 edit)"


def test_a_rejected_verdict_suppresses_the_item_until_it_is_explicitly_cleared(store):
    """Suppressed means out of the way, not deleted, so the next producer cannot re-offer it."""
    item = _offer_one(store)
    rejected = review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="tester")
    assert rejected.suppressed
    assert review.list_items(store).items == ()
    assert [i.item_id for i in review.list_items(store, include_suppressed=True).items] == [
        item.item_id
    ]
    reopened = review.clear(store, item.item_id, actor="tester")
    assert reopened.verdict is None
    assert [i.item_id for i in review.list_items(store).items] == [item.item_id]


def test_a_second_verdict_on_a_settled_item_refuses_rather_than_overwriting(store):
    """Last writer wins is not the same property as a decision being recorded."""
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="first")
    with pytest.raises(CratekitError) as excinfo:
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="second")
    assert excinfo.value.cause.reason == "review-already-resolved"
    assert review.get(store, item.item_id).verdict is review.Verdict.REJECTED
    assert review.get(store, item.item_id).actor == "first"


def test_a_verdict_naming_a_candidate_the_item_never_offered_refuses(store):
    item = _offer_one(store)
    with pytest.raises(CratekitError) as excinfo:
        review.resolve(
            store, item.item_id, review.Verdict.ACCEPTED, option="opt-nowhere", actor="tester"
        )
    assert excinfo.value.cause.reason == "review-option-unknown"
    assert review.get(store, item.item_id).verdict is None


def test_clearing_an_item_that_was_never_resolved_changes_nothing(store):
    item = _offer_one(store)
    assert review.clear(store, item.item_id, actor="tester").verdict is None


# A verdict this build cannot read (P2, KTD21): builds at two versions share the queue,
# and every consumer reads an unknown verdict as unresolved.


def _a_verdict_from_a_newer_build(store, item_id: str, raw: str = "deferred") -> None:
    with store.immediate() as conn:
        conn.execute(
            "UPDATE review_items SET verdict = ? WHERE item_id = ?", (raw, item_id)
        )


def test_an_item_carrying_a_verdict_this_build_cannot_read_is_still_offered(store):
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)
    assert [held.item_id for held in review.list_items(store).items] == [item.item_id]
    assert review.count_unresolved(store) == 1
    assert review.get(store, item.item_id).verdict is None


def test_an_item_carrying_a_verdict_this_build_cannot_read_can_be_resolved(store):
    """It is presented as a question again, so answering it has to land."""
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)
    settled = review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="tester")
    assert settled.verdict is review.Verdict.REJECTED
    assert review.count_unresolved(store) == 0


def test_clearing_an_item_whose_verdict_this_build_cannot_read_clears_the_row(store):
    """``clear`` must not read the COERCED verdict and return before touching the column."""
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)
    review.clear(store, item.item_id, actor="tester")
    assert _stored_verdict(store, item.item_id) is None


def test_an_export_carries_a_verdict_this_build_cannot_read_rather_than_dropping_it(store):
    """Rendered as "no verdict", the next installation would insert the item as open."""
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)
    document = review.export_document(store)
    assert [entry["verdict"] for entry in document["items"]] == ["deferred"]


def test_an_import_does_not_overwrite_a_local_verdict_it_cannot_read(store):
    """The local decision is unreadable, not absent, so it is a conflict."""
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id)
    incoming = _document({**item.to_json(), "verdict": str(review.Verdict.ACCEPTED)})
    result = review.import_document(store, incoming, actor="importer")
    assert result.conflicts == (item.item_id,)
    assert _stored_verdict(store, item.item_id) == "deferred"


def test_quitting_partway_through_a_set_and_returning_presents_only_what_is_left(cfg, store):
    """The plan's second scenario, with a genuine reopen between the two halves."""
    offered = [_offer_one(store, key=f"{index:02d}") for index in range(6)]
    for item in offered[:2]:
        review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="tester")
    review.resolve(store, offered[2].item_id, review.Verdict.REJECTED, actor="tester")
    store.close()
    with review.open_store(cfg) as reopened:
        left = review.list_items(reopened).items
        assert [item.item_id for item in left] == [item.item_id for item in offered[3:]]
        assert review.get(reopened, offered[0].item_id).verdict is review.Verdict.ACCEPTED
        assert review.get(reopened, offered[2].item_id).verdict is review.Verdict.REJECTED
        assert review.count_unresolved(reopened) == 3


# Part 5: batch resolution by predicate


def _mixed_queue(store) -> dict[str, list[str]]:
    """Three kinds across two queues, so a predicate has something to miss."""
    made: dict[str, list[str]] = {}
    for index in range(3):
        item = _offer_one(store, key=f"v{index}", kind="version-difference")
        made.setdefault("version-difference", []).append(item.item_id)
    for index in range(2):
        item = _offer_one(store, key=f"c{index}", kind="clean-cut")
        made.setdefault("clean-cut", []).append(item.item_id)
    for index in range(2):
        item = _offer_one(
            store,
            key=f"g{index}",
            queue=review.Queue.GENRE,
            kind="proposed-genre",
            payload={"confidence": "low"},
        )
        made.setdefault("proposed-genre", []).append(item.item_id)
    return made


def test_batch_resolution_by_predicate_resolves_the_subset_and_leaves_the_rest(store):
    made = _mixed_queue(store)
    settled = review.resolve_where(
        store,
        review.Predicate(kind="version-difference"),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert sorted(item.item_id for item in settled) == sorted(made["version-difference"])
    still_open = {item.item_id for item in review.list_items(store, limit=None).items}
    assert still_open == set(made["clean-cut"]) | set(made["proposed-genre"])


def test_a_predicate_may_select_on_a_payload_field(store):
    _mixed_queue(store)
    settled = review.resolve_where(
        store,
        review.Predicate(queue=review.Queue.GENRE, payload_equals={"confidence": "low"}),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert len(settled) == 2


def test_a_predicate_typed_at_a_command_line_matches_a_payload_number(store):
    """Command line text matches a payload number, or the sweep settles nothing and says success."""
    _offer_one(store, key="numeric", payload={"attempts": 3})
    settled = review.resolve_where(
        store,
        review.Predicate(payload_equals={"attempts": "3"}),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert len(settled) == 1


def test_an_absent_payload_field_is_not_matched_by_the_text_none(store):
    """The one coercion that must NOT happen, or a mistyped field selects every item."""
    _offer_one(store, key="plain", payload={"wanted": "something"})
    settled = review.resolve_where(
        store,
        review.Predicate(payload_equals={"missing_field": "None"}),
        review.Verdict.REJECTED,
        actor="tester",
    )
    assert settled == ()
    assert review.count_unresolved(store) == 1


def test_a_batch_predicate_that_selects_everything_is_refused(store):
    _mixed_queue(store)
    with pytest.raises(CratekitError) as excinfo:
        review.resolve_where(store, review.Predicate(), review.Verdict.ACCEPTED, actor="tester")
    assert excinfo.value.cause.reason == "review-selection-invalid"
    assert review.count_unresolved(store) == 7


def test_batch_resolution_skips_what_is_already_settled_rather_than_refusing(store):
    made = _mixed_queue(store)
    review.resolve(store, made["version-difference"][0], review.Verdict.ACCEPTED, actor="first")
    settled = review.resolve_where(
        store,
        review.Predicate(kind="version-difference"),
        review.Verdict.REJECTED,
        actor="second",
    )
    assert sorted(i.item_id for i in settled) == sorted(made["version-difference"][1:])
    assert review.get(store, made["version-difference"][0]).actor == "first"


def test_a_second_process_sweeping_the_same_predicate_does_not_abort_the_first(cfg, store):
    """Two REAL sweeps over two hundred items: one losing a race does not abort the other."""
    outstanding = set(_offer_many(store, (f"{index:03d}" for index in range(200))))
    store.close()
    running = [
        _start_another_process(
            "--output", "json", "review", "resolve",
            "--where", f"queue={review.Queue.VERSION_MATCH}",
            "--verdict", "rejected", "--actor", f"sweep-{index}",
        )
        for index in range(2)
    ]
    finished = [(process, *process.communicate()) for process in running]
    reported: list[str] = []
    for process, out, err in finished:
        assert process.returncode == int(ExitCode.OK), err or out
        reported.extend(row["id"] for row in json.loads(out)["data"]["items"])
    assert sorted(reported) == sorted(outstanding), "a sweep wrote verdicts it did not report"
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 0


# Part 6: paging, asserted by counting what is built rather than by reading SQL


def _four_hundred(store) -> list[str]:
    return _offer_many(store, (f"{index:04d}" for index in range(400)))


def test_four_hundred_items_page_without_loading_all_of_them_at_once(store, monkeypatch):
    """Counting rows CONVERTED is what tells real paging from reading whole and slicing."""
    made = _four_hundred(store)
    built = 0
    original = review._item_from_row

    def counting(row):
        nonlocal built
        built += 1
        return original(row)

    monkeypatch.setattr(review, "_item_from_row", counting)
    page = review.list_items(store, limit=25)
    assert [item.item_id for item in page.items] == made[:25]
    assert page.next_cursor is not None
    assert built <= 25 + 1, f"{built} items built to show 25: read whole and sliced, not paging"


def test_walking_every_page_visits_each_item_exactly_once(store):
    made = _four_hundred(store)
    seen: list[str] = []
    cursor = None
    while True:
        page = review.list_items(store, limit=37, after=cursor)
        seen.extend(item.item_id for item in page.items)
        if page.next_cursor is None:
            break
        cursor = page.next_cursor
    assert seen == made


def test_a_cursor_is_a_position_so_an_insert_mid_walk_does_not_shift_a_later_page(store):
    """The cursor is an ordinal, so an insert mid walk cannot make a page skip an item."""
    made = [_offer_one(store, key=f"{index:03d}").item_id for index in range(10)]
    first = review.list_items(store, limit=4)
    _offer_one(store, key="inserted-later")
    second = review.list_items(store, limit=4, after=first.next_cursor)
    assert [item.item_id for item in second.items] == made[4:8]


def test_the_walk_used_by_batch_work_holds_one_page_at_a_time(store, monkeypatch):
    """``iter_items``, which export and batch resolution use, holds one page at a time."""
    _four_hundred(store)
    alive = 0
    peak = 0
    original = review.list_items

    def watching(*args, **kwargs):
        nonlocal alive, peak
        page = original(*args, **kwargs)
        alive = len(page.items)
        peak = max(peak, alive)
        return page

    monkeypatch.setattr(review, "list_items", watching)
    assert sum(1 for _ in review.iter_items(store, page=20)) == 400
    assert peak <= 20


@pytest.mark.parametrize("limit", [0, -1, -2])
def test_a_page_size_that_is_not_a_positive_number_is_refused(store, limit):
    """Zero and minus one crashed; minus two is UNBOUNDED in SQLite and read the whole queue."""
    _offer_one(store)
    with pytest.raises(CratekitError) as excinfo:
        review.list_items(store, limit=limit)
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_a_page_size_that_is_not_a_positive_number_is_refused_at_the_command_line(cfg, store):
    _offer_one(store)
    store.close()
    _refused("review", "list", "--limit", "0", reason="review-selection-invalid")


# Part 7: export and import, for anyone who genuinely wants a file


def test_an_export_round_trips_into_an_empty_queue_with_its_verdicts(tmp_path, cfg, store):
    first = _offer_one(store, key="one")
    second = _offer_one(store, key="two")
    review.resolve(store, first.item_id, review.Verdict.REJECTED, actor="tester")
    document = review.export_document(store)
    assert {entry["id"] for entry in document["items"]} == {first.item_id, second.item_id}
    elsewhere = tmp_path / "other" / "queue.db"
    with review.open_store(cfg, path=elsewhere) as receiving:
        result = review.import_document(receiving, document, actor="importer")
        assert sorted(result.inserted) == sorted([first.item_id, second.item_id])
        assert review.get(receiving, first.item_id).verdict is review.Verdict.REJECTED
        assert review.get(receiving, second.item_id).verdict is None


def test_an_import_never_overwrites_a_local_verdict_and_reports_the_conflict(
    tmp_path, cfg, store
):
    """Two people resolving one item differently: the conflict is reported, the local record stands."""
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="local")
    incoming = _document(
        {**item.to_json(), "verdict": str(review.Verdict.REJECTED), "option": None, "actor": "remote"}
    )
    result = review.import_document(store, incoming, actor="importer")
    assert result.conflicts == (item.item_id,)
    assert review.get(store, item.item_id).verdict is review.Verdict.ACCEPTED
    assert review.get(store, item.item_id).actor == "local"


def test_an_export_written_by_another_version_refuses(store):
    with pytest.raises(CratekitError) as excinfo:
        review.import_document(store, {"export": 99, "items": []}, actor="importer")
    assert excinfo.value.cause.reason == "review-file-unusable"


def test_one_unapplicable_item_does_not_abort_the_import(tmp_path, cfg, store):
    """Two items refused for different reasons either side of a good one; the good one applies."""
    good = _offer_one(store, key="good").to_json()
    document = _document(
        # A verdict this build has no representation for.
        {**good, "id": "rv_unreadable", "verdict": "whatever-that-means"},
        {**good, "verdict": str(review.Verdict.ACCEPTED), "option": "opt-accept"},
        # A candidate the item never offered, which ``resolve`` refuses.
        {
            **good,
            "id": "rv_bad_option",
            "options": [],
            "verdict": str(review.Verdict.ACCEPTED),
            "option": "opt-nowhere",
        },
    )
    elsewhere = tmp_path / "receiving" / "queue.db"
    with review.open_store(cfg, path=elsewhere) as receiving:
        result = review.import_document(receiving, document, actor="importer")
        assert sorted(result.conflicts) == ["rv_bad_option", "rv_unreadable"]
        assert review.get(receiving, good["id"]).verdict is review.Verdict.ACCEPTED


@pytest.mark.parametrize(
    ("name", "broken"),
    [
        ("a payload that is not a mapping", {"payload": [1, 2, 3]}),
        ("an option with no identifier", {"options": [{"summary": "no identifier here"}]}),
        ("a queue nobody declared", {"queue": "invented"}),
        ("options that are not a list", {"options": 7}),
    ],
)
def test_a_malformed_item_is_reported_rather_than_raised_out_of_the_import(
    tmp_path, cfg, store, name, broken
):
    """An import is TOTAL: a type or key error must not abort it after earlier items were written."""
    good = _offer_one(store, key="good").to_json()
    document = _document(
        {**good, "id": "rv_broken", **broken},
        {**good, "verdict": str(review.Verdict.ACCEPTED), "option": "opt-accept"},
    )
    elsewhere = tmp_path / "receiving" / "queue.db"
    with review.open_store(cfg, path=elsewhere) as receiving:
        result = review.import_document(receiving, document, actor="importer")
        assert result.conflicts == ("rv_broken",), name
        assert review.get(receiving, good["id"]).verdict is review.Verdict.ACCEPTED


def test_an_import_says_why_each_item_it_could_not_apply_was_not_applied(tmp_path, cfg, store):
    """Each conflict carries its own reason; "the export disagrees" is only one of them."""
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="local")
    document = _document(
        {**item.to_json(), "verdict": str(review.Verdict.REJECTED), "actor": "remote"},
        {**item.to_json(), "id": "rv_unreadable", "verdict": "whatever-that-means"},
        {**item.to_json(), "id": "rv_broken", "payload": [1, 2, 3]},
    )
    result = review.import_document(store, document, actor="importer")
    assert set(result.conflicts) == {"rv_broken", "rv_unreadable", item.item_id}
    assert set(result.reasons) == set(result.conflicts), "every conflict carries a reason"
    assert len(set(result.reasons.values())) == 3, (
        f"three failures collapsed into {set(result.reasons.values())}"
    )


def test_an_unresolved_cause_says_how_many_are_outstanding_and_what_to_do():
    """One sentence for "a person still has to decide", built in one place."""
    cause = review.unresolved_cause(4)
    assert cause.code is ExitCode.PENDING_HUMAN
    assert cause.detail["unresolved"] == 4
    assert cause.remediation.steps


# Part 7b: SUPERSEDED, written by the resolution that owned the row, never by a person.


def test_supersede_retires_an_open_item_naming_the_rule_and_it_leaves_the_open_list(store):
    item = _offer_one(store)
    (retired,) = review.supersede(store, [item.item_id], rule="isrc-exact")
    assert retired.verdict is review.Verdict.SUPERSEDED
    assert retired.actor == "isrc-exact"
    assert retired.option is None
    assert retired.decided
    assert retired.resolved
    # Not a suppression: the question ceased to be one.
    assert not retired.suppressed
    assert [one.item_id for one in review.list_items(store)] == []
    assert [one.item_id for one in review.list_items(store, include_suppressed=True)] == []
    assert [one.item_id for one in review.list_items(store, include_resolved=True)] == [
        item.item_id
    ]
    assert review.count_unresolved(store) == 0


def test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them(store):
    """Unfiled, answered and repeated identifiers in one call; only the open ones retire."""
    first = _offer_one(store, key="a")
    second = _offer_one(store, key="b")
    third = _offer_one(store, key="c")
    review.resolve(store, second.item_id, review.Verdict.ACCEPTED, actor="phillip")
    retired = review.supersede(
        store,
        [first.item_id, second.item_id, "rv_never_offered", third.item_id, first.item_id],
        rule="isrc-exact",
    )
    assert [one.item_id for one in retired] == [first.item_id, third.item_id]
    assert all(one.verdict is review.Verdict.SUPERSEDED for one in retired)
    assert review.get(store, second.item_id).actor == "phillip"
    assert review.supersede(store, [], rule="isrc-exact") == ()


@pytest.mark.parametrize("theirs", [review.Verdict.ACCEPTED, review.Verdict.REJECTED])
def test_supersede_never_overwrites_a_persons_verdict(store, theirs):
    """The brief's fourth scenario: a person's verdict stands and the call reports nothing."""
    item = _offer_one(store)
    review.resolve(store, item.item_id, theirs, actor="phillip")
    assert review.supersede(store, [item.item_id], rule="isrc-exact") == ()
    kept = review.get(store, item.item_id)
    assert kept.verdict is theirs
    assert kept.actor == "phillip"


def test_supersede_never_overwrites_a_verdict_this_build_cannot_read(store):
    """Narrower than resolve on purpose: a newer build's value is somebody's decision."""
    item = _offer_one(store)
    _a_verdict_from_a_newer_build(store, item.item_id, "from-a-newer-build")
    assert review.get(store, item.item_id).verdict is None, "the reader sees a question"
    assert review.supersede(store, [item.item_id], rule="isrc-exact") == ()
    assert review.get(store, item.item_id).stored_verdict == "from-a-newer-build"


def test_supersede_reports_nothing_for_an_item_nobody_filed(store):
    assert review.supersede(store, ["rv_never_offered"], rule="isrc-exact") == ()


def test_supersede_refuses_an_empty_rule(store):
    item = _offer_one(store)
    with pytest.raises(CratekitError) as caught:
        review.supersede(store, [item.item_id], rule="")
    assert caught.value.cause.reason == "review-selection-invalid"
    assert review.get(store, item.item_id).verdict is None


def test_resolve_and_the_batch_refuse_the_machines_verdict(store):
    """The third verdict has one writer; ``resolve``, the batch and the import ride on a person's path."""
    item = _offer_one(store)
    with pytest.raises(CratekitError) as caught:
        review.resolve(store, item.item_id, review.Verdict.SUPERSEDED, actor="phillip")
    assert caught.value.cause.reason == "review-selection-invalid"
    with pytest.raises(CratekitError):
        review.resolve_where(
            store,
            review.Predicate(queue=review.Queue.VERSION_MATCH),
            review.Verdict.SUPERSEDED,
            actor="phillip",
        )
    assert review.get(store, item.item_id).verdict is None


def test_a_superseded_item_offered_again_is_neither_reopened_nor_duplicated(store):
    """The brief's second scenario: the third verdict is a resolution, so offer leaves it alone."""
    item = _offer_one(store)
    review.supersede(store, [item.item_id], rule="isrc-exact")
    again = _offer_one(store, payload={"wanted": "track a", "found": "a newer description"})
    assert again.item_id == item.item_id
    assert again.verdict is review.Verdict.SUPERSEDED
    assert again.actor == "isrc-exact"
    assert again.payload == item.payload, "a resolved item's payload is left alone"
    assert len(review.list_items(store, include_resolved=True, limit=None)) == 1


def test_clear_returns_a_superseded_item_to_the_open_list(store):
    """The brief's third scenario. Revocable like any verdict."""
    item = _offer_one(store)
    review.supersede(store, [item.item_id], rule="isrc-exact")
    cleared = review.clear(store, item.item_id, actor="phillip")
    assert cleared.verdict is None
    assert cleared.actor == "phillip"
    assert [one.item_id for one in review.list_items(store)] == [item.item_id]


def test_a_batch_resolution_does_not_touch_items_a_resolution_superseded(store):
    """The brief's sixth scenario: a sweep filters what is outstanding and leaves superseded items."""
    first = _offer_one(store, key="a", payload={"why": "title-approximate"})
    second = _offer_one(store, key="b", payload={"why": "title-approximate"})
    review.supersede(store, [first.item_id], rule="isrc-exact")
    swept = review.resolve_where(
        store,
        review.Predicate(queue=review.Queue.VERSION_MATCH, payload_equals={"why": "title-approximate"}),
        review.Verdict.REJECTED,
        actor="phillip",
    )
    assert [one.item_id for one in swept] == [second.item_id]
    untouched = review.get(store, first.item_id)
    assert untouched.verdict is review.Verdict.SUPERSEDED
    assert untouched.actor == "isrc-exact"


def test_an_export_carrying_the_third_verdict_imports_without_conflict(cfg, store, tmp_path):
    """The brief's fifth scenario: into a queue that never saw the item, and back into its writer."""
    item = _offer_one(store)
    review.supersede(store, [item.item_id], rule="credited-exact")
    document = review.export_document(store)
    assert document["items"][0]["verdict"] == "superseded"
    with review.open_store(cfg, path=tmp_path / "elsewhere.sqlite3") as other:
        taken = review.import_document(other, document, actor="importer")
        assert taken.conflicts == ()
        assert taken.inserted == (item.item_id,)
        landed = review.get(other, item.item_id)
        assert landed.verdict is review.Verdict.SUPERSEDED
        assert landed.actor == "credited-exact"
        assert [one.item_id for one in review.list_items(other)] == []
    back = review.import_document(store, document, actor="importer")
    assert back.conflicts == ()
    assert back.unchanged == (item.item_id,)


def test_an_import_carries_the_machines_verdict_under_the_machines_rules(cfg, store, tmp_path):
    """An incoming superseded verdict lands through ``supersede``; one naming no rule is not applied."""
    item = _offer_one(store)
    edited = _document(
        {**item.to_json(), "verdict": "superseded", "option": "opt-accept", "actor": "isrc-exact"},
        exported="2026-09-23T00:00:00Z",
    )
    taken = review.import_document(store, edited, actor="importer")
    assert taken.conflicts == ()
    landed = review.get(store, item.item_id)
    assert landed.verdict is review.Verdict.SUPERSEDED
    assert landed.actor == "isrc-exact"
    assert landed.option is None
    other = _offer_one(store, key="b")
    unnamed = {**edited, "items": [{**other.to_json(), "verdict": "superseded", "actor": ""}]}
    taken = review.import_document(store, unnamed, actor="importer")
    assert taken.reasons == {other.item_id: review.CONFLICT_NOT_APPLIED}
    assert review.get(store, other.item_id).verdict is None


def test_the_command_line_offers_a_person_only_the_persons_verdicts(store, capsys):
    """``PERSON_VERDICTS`` is the parser's vocabulary; argparse's refusal is read through ``capsys``."""
    assert review.PERSON_VERDICTS == (review.Verdict.ACCEPTED, review.Verdict.REJECTED)
    item = _offer_one(store)
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(
        ["--output", "json", "review", "resolve", item.item_id, "--verdict", "superseded"],
        stdout=out,
        stderr=err,
    )
    assert code == 2
    assert "invalid choice: 'superseded'" in capsys.readouterr().err
    assert review.get(store, item.item_id).verdict is None


# Part 8: the decision stores, which share this shape and are revocable


def test_the_decision_stores_are_the_two_the_state_inventory_declares(cfg):
    """DERIVED from the inventory (P3), and still holding R35's and R36's two stores."""
    declared = tuple(sorted(entry.key for entry in config.STATE_FILES if entry.decision_store))
    assert review.DECISION_STORE_KEYS == declared, (
        "the module's list has drifted from the inventory"
    )
    # Against the derived set, so a derivation that lost both is not vacuously equal.
    assert {"declines", "tombstones"} <= set(declared)
    for key in review.DECISION_STORE_KEYS:
        entry = config.state_file(key)
        assert entry.root is config.StateRoot.LIBRARY
        assert entry.snapshot is config.SnapshotRole.COUPLED, (
            f"{key} must roll back with the database"
        )
        assert review.DecisionStore(key, cfg).path == config.state_path(key, cfg)


def test_a_decline_suppresses_and_is_revocable(cfg):
    """R35: remembered, never offered again, until revoked; revoked records are kept."""
    declines = review.DecisionStore("declines", cfg)
    identity = {"device": 12, "inode": 3456}
    assert not declines.suppresses("removed-file", identity)
    recorded = declines.record(kind="removed-file", identity=identity, actor="tester")
    assert declines.suppresses("removed-file", identity)
    assert [d.suppression_id for d in declines.suppressions()] == [recorded.suppression_id]
    declines.revoke(recorded.suppression_id, actor="tester")
    assert not declines.suppresses("removed-file", identity)
    assert declines.suppressions() == ()
    assert [d.suppression_id for d in declines.suppressions(include_revoked=True)] == [
        recorded.suppression_id
    ]


def test_recording_a_suppression_twice_changes_nothing(cfg):
    tombstones = review.DecisionStore("tombstones", cfg)
    identity = {"recording": "abc", "version": "original"}
    first = tombstones.record(kind="version", identity=identity, actor="tester")
    again = tombstones.record(kind="version", identity=identity, actor="somebody-else")
    assert again == first


def test_a_revoked_suppression_can_be_recorded_again(cfg):
    tombstones = review.DecisionStore("tombstones", cfg)
    identity = {"recording": "abc", "version": "original"}
    first = tombstones.record(kind="version", identity=identity, actor="tester")
    tombstones.revoke(first.suppression_id, actor="tester")
    assert tombstones.record(kind="version", identity=identity, actor="tester").suppressing


def test_the_two_stores_do_not_share_an_identifier_space(cfg):
    """A decline and a tombstone about the same thing are different decisions."""
    identity = {"recording": "abc"}
    assert review.suppression_id_for("declines", "version", identity) != (
        review.suppression_id_for("tombstones", "version", identity)
    )


def test_a_suppression_identifier_is_not_mistakable_for_a_review_item(cfg):
    assert review.suppression_id_for("declines", "k", {"a": 1}).startswith(
        review.SUPPRESSION_ID_PREFIX
    )
    assert review.item_id_for(review.Queue.DELETION, "k", {"a": 1}).startswith(review.ID_PREFIX)


def test_an_unreadable_decision_store_refuses_rather_than_reading_as_empty(cfg):
    """A tolerant read on a path that governs an action fails OPEN (U8's lesson)."""
    declines = review.DecisionStore("declines", cfg)
    declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    declines.path.write_text("{not json at all")
    with pytest.raises(CratekitError) as excinfo:
        declines.suppresses("removed-file", {"inode": 1})
    assert excinfo.value.cause.reason == "review-file-unusable"


def _declines_holding(cfg, text: str):
    declines = review.DecisionStore("declines", cfg)
    declines.path.parent.mkdir(parents=True, exist_ok=True)
    declines.path.write_text(text)
    return declines


def _declines_document(**fields) -> str:
    return json.dumps({"version": 1, "store": "declines", "decisions": [], **fields})


#: Good JSON that is not this store, each once read as empty and then overwritten.
STRUCTURALLY_WRONG_STORES = {
    "a top level list": "[]",
    "a top level scalar": "7",
    "a version this build does not know": _declines_document(version=99),
    "no version at all": json.dumps({"store": "declines", "decisions": []}),
    "records under another version's key": json.dumps(
        {"version": 1, "store": "declines", "records": []}
    ),
    "decisions present and null": _declines_document(decisions=None),
    "decisions that are not a list": _declines_document(decisions={"dc_one": {}}),
    "another store's document": _declines_document(store="tombstones"),
    "a record whose identifier key was renamed": _declines_document(
        decisions=[{"identifier": "dc_one"}]
    ),
    "a record whose payload is not a mapping": _declines_document(
        decisions=[{"id": "dc_one", "payload": 5}]
    ),
    "a record that is not a mapping": _declines_document(decisions=["dc_one"]),
}


@pytest.mark.parametrize("shape", sorted(STRUCTURALLY_WRONG_STORES))
def test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten(cfg, shape):
    """Refusal is the only alternative to a correct read, and no later write may replace the file."""
    declines = _declines_holding(cfg, STRUCTURALLY_WRONG_STORES[shape])
    before = declines.path.read_text()
    with pytest.raises(CratekitError) as excinfo:
        declines.suppressions()
    assert excinfo.value.cause.reason == "review-file-unusable"
    with pytest.raises(CratekitError):
        declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    assert declines.path.read_text() == before
    with pytest.raises(CratekitError):
        declines.revoke("dc_one", actor="tester")
    assert declines.path.read_text() == before


def test_a_record_whose_payload_is_not_a_mapping_refuses_rather_than_raising(cfg):
    """``suppresses`` is asked once per candidate, so a type error out of it kills the pass."""
    declines = _declines_holding(
        cfg, _declines_document(decisions=[{"id": "dc_one", "payload": [1, 2, 3]}])
    )
    with pytest.raises(CratekitError) as excinfo:
        declines.suppresses("removed-file", {"inode": 1})
    assert excinfo.value.cause.reason == "review-file-unusable"


# Two processes, which is the case a document store has to survive

_IN_A_CHILD = """
import sys

from cratekit.core import config, review

key, worker, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
store = review.DecisionStore(key, config.load())
for index in range(count):
"""

_RECORD_IN_A_CHILD = _IN_A_CHILD + """    store.record(
        kind="version",
        identity={"worker": worker, "index": index},
        actor="worker-" + str(worker),
    )
"""

_REVOKE_IN_A_CHILD = _IN_A_CHILD + """    store.revoke(
        review.suppression_id_for(key, "version", {"worker": worker, "index": index}),
        actor="worker-" + str(worker),
    )
"""

#: The reviewer's numbers: unlocked, 78 of 200 records reached the disk.
WORKERS = 8
PER_WORKER = 25


def test_every_decision_and_revocation_by_eight_processes_at_once_survives(cfg):
    """Eight processes record, then revoke, into each store at once, and nothing is lost."""
    _all_succeed(
        [
            *_start_separate_processes(
                _RECORD_IN_A_CHILD,
                workers=WORKERS,
                arguments=lambda worker: ("tombstones", worker, PER_WORKER),
            ),
            *_start_separate_processes(
                _RECORD_IN_A_CHILD,
                workers=WORKERS,
                arguments=lambda worker: ("declines", worker, PER_WORKER),
            ),
        ]
    )
    held = review.DecisionStore("tombstones", cfg).suppressions()
    assert len(held) == WORKERS * PER_WORKER, (
        f"{len(held)} of {WORKERS * PER_WORKER} reported decisions reached the disk"
    )
    _all_succeed(
        _start_separate_processes(
            _REVOKE_IN_A_CHILD,
            workers=WORKERS,
            arguments=lambda worker: ("declines", worker, PER_WORKER),
        )
    )
    declines = review.DecisionStore("declines", cfg)
    assert declines.suppressions() == ()
    assert len(declines.suppressions(include_revoked=True)) == WORKERS * PER_WORKER


def test_a_mode_the_filesystem_refuses_is_reported_rather_than_swallowed(cfg, monkeypatch):
    """A refused chmod would leave a world readable queue with nothing raised."""
    real_chmod = os.chmod
    target = review.queue_path(cfg)

    def refusing(path, mode, *args, **kwargs):
        if str(path).startswith(str(target)):
            raise PermissionError(1, "operation not permitted")
        return real_chmod(path, mode, *args, **kwargs)

    monkeypatch.setattr(os, "chmod", refusing)
    with pytest.raises(CratekitError) as excinfo:
        review.open_store(cfg)
    assert excinfo.value.cause.reason == "review-file-unusable"


@pytest.fixture
def permissive_umask():
    """Run the body under umask 000, then put the process back."""
    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


def test_every_path_this_unit_creates_is_private_under_any_umask(permissive_umask, cfg):
    """P1 over the queue, the decision store documents and their locks, derived by walking."""
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    with review.open_store(cfg) as store:
        _offer_one(store)
    declines = review.DecisionStore("declines", cfg)
    recorded = declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    declines.revoke(recorded.suppression_id, actor="tester")
    roots = [
        config.state_path("review_queue", cfg),
        declines.path.parent,
        declines.lock_path.parent,
    ]
    checked = 0
    for root in roots:
        for path in [root, *root.rglob("*")]:
            mode = path.stat().st_mode & 0o777
            expected = config.PRIVATE_DIR_MODE if path.is_dir() else config.PRIVATE_FILE_MODE
            assert mode == expected, f"{path} landed {oct(mode)}"
            checked += 1
    assert checked >= 6, "the walk found less than this unit is known to write"


def test_a_decision_store_lands_owner_only_whatever_the_umask(cfg):
    declines = review.DecisionStore("declines", cfg)
    declines.record(kind="removed-file", identity={"inode": 1}, actor="tester")
    if hasattr(os, "chmod"):
        assert declines.path.stat().st_mode & 0o777 == config.PRIVATE_FILE_MODE
        assert declines.path.parent.stat().st_mode & 0o777 == config.PRIVATE_DIR_MODE


def test_a_store_the_inventory_does_not_declare_is_refused(cfg):
    with pytest.raises(CratekitError) as excinfo:
        review.DecisionStore("whatever", cfg)
    assert excinfo.value.cause.reason == "review-queue-undeclared"


# Part 9: the unit's verification


def test_a_match_producing_all_three_states_round_trips_across_two_processes(cfg, store):
    """The unit's verification (R11): half answered, a restart, another process answers the rest."""
    matched = [{"row": "1", "state": "matched"}]
    needs_review = [{"row": "2", "state": "needs_review"}, {"row": "3", "state": "needs_review"}]
    missing = [{"row": "4", "state": "missing"}]
    offered = [
        review.offer(
            store,
            queue=review.Queue.VERSION_MATCH,
            kind="version-difference",
            identity={"source": "list-9", "row": row["row"]},
            payload=dict(row),
            options=(review.Option(option_id="opt-same", summary="the same recording"),),
            handler_key="match.run",
        )
        for row in needs_review
    ]
    assert review.count_unresolved(store) == len(needs_review)
    # By identity rather than by count, so an item under another kind is caught.
    for row in matched + missing:
        absent = review.item_id_for(
            review.Queue.VERSION_MATCH, "version-difference", {"source": "list-9", "row": row["row"]}
        )
        with pytest.raises(CratekitError):
            review.get(store, absent)
    review.resolve(
        store, offered[0].item_id, review.Verdict.ACCEPTED, option="opt-same", actor="person"
    )
    store.close()
    done = _in_another_process(
        "--output", "json", "review", "resolve", offered[1].item_id, "--verdict", "rejected"
    )
    assert done.returncode == 0, done.stderr
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 0
        assert review.get(reopened, offered[0].item_id).verdict is review.Verdict.ACCEPTED
        assert review.get(reopened, offered[1].item_id).verdict is review.Verdict.REJECTED
        assert review.get(reopened, offered[1].item_id).suppressed


# Part 10: the verbs, and the structured output R32 requires of them


def test_the_review_set_output_validates_against_its_committed_schema(cfg, store):
    """The plan's sixth scenario, against the product's own check and the SHIPPED schema."""
    _offer_one(store)
    store.close()
    code, envelope, _ = _drive("review", "list")
    assert code == int(ExitCode.OK)
    assert output.envelope_problems(envelope) == [], envelope
    assert envelope["schema"] == "review_set/1"
    declared = json.loads((SCHEMA_DIR / "review_set.v1.json").read_text())
    payload = envelope["data"]
    assert sorted(payload) == declared["required"]
    assert declared["additionalProperties"] is False
    assert payload["unresolved"] == 1
    assert payload["items"][0]["kind"] == "version-difference"


def test_listing_shows_what_is_outstanding_and_not_what_is_settled(cfg, store):
    open_item = _offer_one(store, key="open")
    settled = _offer_one(store, key="settled")
    review.resolve(store, settled.item_id, review.Verdict.ACCEPTED, actor="tester")
    store.close()
    _, outstanding, _ = _drive("review", "list")
    assert [row["id"] for row in outstanding["data"]["items"]] == [open_item.item_id]
    assert outstanding["data"]["unresolved"] == 1
    _, everything, _ = _drive("review", "list", "--all")
    assert {row["id"] for row in everything["data"]["items"]} == {
        open_item.item_id,
        settled.item_id,
    }
    # The backlog is a query over the queue, never the length of the page.
    assert everything["data"]["unresolved"] == 1


def test_an_empty_queue_is_a_no_op_rather_than_a_failure(cfg, store):
    store.close()
    code, envelope, _ = _drive("review", "list")
    assert code == int(ExitCode.OK)
    assert envelope["outcome"] == "no_op"


def test_showing_one_item_carries_its_whole_record(cfg, store):
    item = _offer_one(store)
    store.close()
    code, envelope, _ = _drive("review", "show", item.item_id)
    assert code == int(ExitCode.OK)
    shown = envelope["data"]["items"][0]
    assert shown["payload"] == dict(item.payload)
    assert [option["option_id"] for option in shown["options"]] == ["opt-accept", "opt-other"]
    assert envelope["data"]["queue"] == str(review.Queue.VERSION_MATCH)


def test_an_unknown_identifier_refuses_with_a_code_from_the_vocabulary(cfg, store):
    store.close()
    _refused("review", "show", "rv_nothing", reason="review-item-unknown")


def test_a_batch_resolution_from_the_command_line_settles_only_the_subset(cfg, store):
    made = _mixed_queue(store)
    store.close()
    code, envelope, _ = _drive(
        "review", "resolve", "--where", "kind=version-difference", "--verdict", "rejected"
    )
    assert code == int(ExitCode.OK)
    assert {row["id"] for row in envelope["data"]["items"]} == set(made["version-difference"])
    assert envelope["data"]["unresolved"] == 4


def test_a_predicate_on_a_payload_field_is_reachable_from_the_command_line(cfg, store):
    _mixed_queue(store)
    store.close()
    code, envelope, _ = _drive(
        "review", "resolve",
        "--where", "queue=genre",
        "--where", "payload.confidence=low",
        "--verdict", "rejected",
    )
    assert code == int(ExitCode.OK)
    assert len(envelope["data"]["items"]) == 2


def test_a_resolution_naming_both_an_item_and_a_predicate_refuses(cfg, store):
    item = _offer_one(store)
    store.close()
    _refused(
        "review", "resolve", item.item_id, "--where", "kind=x", "--verdict", "accepted",
        reason="review-selection-invalid",
    )


def test_a_batch_resolution_naming_a_candidate_refuses_rather_than_dropping_it(cfg, store):
    """Each item offers its own candidates, so one identifier cannot span a subset."""
    _mixed_queue(store)
    store.close()
    _refused(
        "review", "resolve", "--where", "kind=version-difference",
        "--verdict", "accepted", "--option", "opt-accept",
        reason="review-selection-invalid",
    )
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 7


def test_a_resolution_naming_neither_refuses_rather_than_answering_everything(cfg, store):
    _offer_one(store)
    store.close()
    _refused("review", "resolve", "--verdict", "accepted", reason="review-selection-invalid")
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 1


def test_a_malformed_predicate_is_refused_rather_than_matching_nothing(cfg, store):
    """A filter that silently matches nothing looks exactly like an empty queue."""
    _offer_one(store)
    store.close()
    for bad in ("kind", "nonsense=1"):
        _refused(
            "review", "resolve", "--where", bad, "--verdict", "accepted",
            reason="review-selection-invalid",
        )


def test_clearing_from_the_command_line_puts_a_rejected_item_back(cfg, store):
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.REJECTED, actor="tester")
    store.close()
    code, envelope, _ = _drive("review", "clear", item.item_id, "--actor", "somebody")
    assert code == int(ExitCode.OK)
    assert envelope["data"]["items"][0]["verdict"] is None
    with review.open_store(cfg) as reopened:
        assert review.count_unresolved(reopened) == 1


def test_an_export_and_an_import_round_trip_through_the_command_line(
    tmp_path, cfg, store, monkeypatch
):
    first = _offer_one(store, key="one")
    second = _offer_one(store, key="two")
    review.resolve(store, first.item_id, review.Verdict.REJECTED, actor="tester")
    store.close()
    target = tmp_path / "exports" / "queue.json"
    code, envelope, _ = _drive("review", "export", str(target))
    assert code == int(ExitCode.OK)
    assert target.exists()
    assert {row["id"] for row in envelope["data"]["items"]} == {first.item_id, second.item_id}
    # A transport, not an editing surface: versioned JSON.
    document = json.loads(target.read_text())
    assert document["export"] == review.EXPORT_VERSION
    # A SECOND library, reached as a relocation is, since an environment override
    # relocates any hand built Config straight back to this one.
    elsewhere = tmp_path / "second-library"
    (elsewhere / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(elsewhere))
    config.reset_cache()
    moved = config.load()
    assert moved.library.root == elsewhere
    code, imported, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert {row["id"] for row in imported["data"]["items"]} == {first.item_id, second.item_id}
    with review.open_store(moved) as receiving:
        assert review.get(receiving, first.item_id).verdict is review.Verdict.REJECTED
        assert review.count_unresolved(receiving) == 1


def test_an_export_never_replaces_a_file_that_is_already_there(tmp_path, cfg, store):
    """Refusing is what keeps this verb out of the destructive class entirely."""
    _offer_one(store)
    store.close()
    target = tmp_path / "already-here.json"
    target.write_text("something somebody wanted")
    _refused("review", "export", str(target), reason="review-file-unusable")
    assert target.read_text() == "something somebody wanted"


def test_an_import_reports_a_conflict_as_a_warning_and_keeps_the_local_verdict(
    tmp_path, cfg, store
):
    item = _offer_one(store)
    review.resolve(store, item.item_id, review.Verdict.ACCEPTED, actor="local")
    store.close()
    target = _written(
        tmp_path / "incoming.json",
        {**item.to_json(), "verdict": str(review.Verdict.REJECTED), "option": None, "actor": "remote"},
    )
    code, envelope, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert [warning["code"] for warning in envelope["warnings"]] == ["review-verdict-conflict"]
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, item.item_id).actor == "local"


def test_an_import_that_applies_one_verdict_and_cannot_apply_another_reports_both(
    tmp_path, cfg, store
):
    """It reports what it applied plus a warning, never failure after writing, and reruns succeed."""
    item = _offer_one(store)
    store.close()
    target = _written(
        tmp_path / "incoming.json",
        {**item.to_json(), "verdict": str(review.Verdict.ACCEPTED)},
        {**item.to_json(), "id": "rv_from_a_newer_build", "verdict": "whatever-that-means"},
    )
    code, envelope, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert [row["id"] for row in envelope["data"]["items"]] == [item.item_id], (
        "an identifier it never took in is not something it applied"
    )
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "review-verdict-conflict"
    ]
    assert "rv_from_a_newer_build" in envelope["warnings"][0]["message"]
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, item.item_id).verdict is review.Verdict.ACCEPTED
    again, second, _ = _drive("review", "import", str(target))
    assert again == int(ExitCode.OK)


def test_an_import_lists_an_item_it_inserted_and_could_not_settle_exactly_once(
    tmp_path, cfg, store
):
    """Inserted and not settled is in both lists, and is still one item."""
    good = _offer_one(store, key="good").to_json()
    store.close()
    target = _written(
        tmp_path / "incoming.json",
        {
            **good,
            "id": "rv_no_such_option",
            "options": [],
            "verdict": str(review.Verdict.ACCEPTED),
            "option": "opt-nowhere",
        },
    )
    code, envelope, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert [row["id"] for row in envelope["data"]["items"]] == ["rv_no_such_option"]


def test_an_import_carrying_a_malformed_item_does_not_fail_as_an_internal_error(
    tmp_path, cfg, store
):
    """An internal error is a bare status with no cause, which the vocabulary exists to forbid."""
    good = _offer_one(store, key="good").to_json()
    store.close()
    target = _written(
        tmp_path / "incoming.json",
        {**good, "id": "rv_broken", "payload": [1, 2, 3]},
        {**good, "verdict": str(review.Verdict.REJECTED)},
    )
    code, envelope, _ = _drive("review", "import", str(target))
    assert code == int(ExitCode.OK)
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "review-verdict-conflict"
    ]
    with review.open_store(cfg) as reopened:
        assert review.get(reopened, good["id"]).verdict is review.Verdict.REJECTED


def test_every_reason_an_import_can_report_has_a_sentence_a_person_can_act_on():
    """DERIVED by introspecting the module, so a new reason cannot arrive mute."""
    from cratekit.cli import review as verbs
    declared = {
        value
        for name, value in vars(review).items()
        if name.startswith("CONFLICT_") and isinstance(value, str)
    }
    assert declared, "the reasons are no longer discoverable by introspection"
    missing = declared - set(verbs.CONFLICT_SENTENCES)
    assert not missing, f"conflict reasons with no sentence for the user: {sorted(missing)}"
    assert set(verbs.CONFLICT_SENTENCES) == declared, (
        f"sentences for reasons the core cannot report: {sorted(set(verbs.CONFLICT_SENTENCES) - declared)}"
    )


def test_an_import_of_something_that_is_not_an_export_refuses(tmp_path, cfg, store):
    store.close()
    target = tmp_path / "not-an-export.json"
    target.write_text("[]")
    _refused("review", "import", str(target), reason="review-file-unusable")


def test_an_import_of_a_file_that_is_not_there_refuses_by_name(tmp_path, cfg, store):
    store.close()
    _refused("review", "import", str(tmp_path / "absent.json"), reason="review-file-unusable")


# R33's "never reads standard input" is asserted over every module by test_cli_contract.


# Part 11: what this unit settled that a LATER unit owes (P5)
# Each guard resolves a call to THIS module through the import graph, never by
# attribute name, which once matched an unrelated ``_Ranking.offer`` (P7).

#: The reviewer's evasion: adjudicates nothing, hand edits the comma separated
#: file R12 replaces behind an aliased import, and satisfies a name match.
EVASION_SOURCE = '''
"""A module that answers a name matching countdown and adjudicates nothing."""

import csv as spreadsheet

from cratekit.core import review

_PLANNED_QUEUE = review.Queue.VERSION_MATCH


class _Ranking:
    def offer(self, candidate):
        return candidate


def run(rows, handle):
    ranking = _Ranking()
    writer = spreadsheet.DictWriter(handle, ["wanted", "found", "gate"])
    for row in rows:
        writer.writerow({**row, "gate": ranking.offer(row)["found"]})
'''

#: Correct code, module import shape.
CORRECT_OFFER_MODULE_IMPORT = '''
from cratekit.core import review


def run(store, needing_review):
    for candidate in needing_review:
        review.offer(
            store,
            queue=review.Queue.VERSION_MATCH,
            kind="version-difference",
            identity=candidate.identity,
            payload=candidate.payload,
        )
'''

#: Correct code, symbol import shape, with the queue held in a module constant.
CORRECT_OFFER_SYMBOL_IMPORT = '''
from cratekit.core.review import Queue, offer

QUEUE = Queue.VERSION_MATCH


def run(store, needing_review):
    for candidate in needing_review:
        offer(
            store,
            queue=QUEUE,
            kind="version-difference",
            identity=candidate.identity,
            payload=candidate.payload,
        )
'''

# The relative spellings a SIBLING of the review module would use.

#: A sibling importing the symbol; ``node.module`` holds only ``review``.
CORRECT_OFFER_SIBLING_RELATIVE_IMPORT = '''
from .review import Queue, offer


def run(store, needing_review):
    for candidate in needing_review:
        offer(store, queue=Queue.VERSION_MATCH, identity=candidate.identity)
'''

#: A sibling importing the module; ``node.module`` is None.
CORRECT_OFFER_SIBLING_BOUND_AS_A_MODULE = '''
from . import review


def run(store, needing_review):
    for candidate in needing_review:
        review.offer(
            store, queue=review.Queue.VERSION_MATCH, identity=candidate.identity
        )
'''

#: Two levels up, the ONE relative spelling the old rule recognized.
CORRECT_OFFER_RELATIVE_IMPORT_TWO_LEVELS_UP = CORRECT_OFFER_SIBLING_RELATIVE_IMPORT.replace(
    "from .review import", "from ..core.review import"
)

#: The same text as the sibling fixture, read in ANOTHER package whose own
#: sibling is called ``review``: the resolution must answer no, a suffix match cannot.
EVASION_A_DIFFERENT_SIBLING_CALLED_REVIEW = CORRECT_OFFER_SIBLING_BOUND_AS_A_MODULE

#: Correct code holding a decision store on a field, which is the ordinary shape.
CORRECT_DECISION_STORE = '''
from cratekit.core import review


class DeletionPass:
    def __init__(self, cfg):
        self.declines = review.DecisionStore("declines", cfg)

    def decline(self, identity):
        self.declines.record(kind="removed-file", identity=identity, actor="cli")

    def undo(self, suppression_id):
        self.declines.revoke(suppression_id, actor="cli")
'''

#: Correct code reaching the store through a small helper, one hop further out.
CORRECT_DECISION_STORE_VIA_HELPER = '''
from cratekit.core.review import DecisionStore


def _tombstones(cfg):
    return DecisionStore("tombstones", cfg)


def run(cfg, identity, suppression_id):
    store = _tombstones(cfg)
    store.record(kind="version", identity=identity, actor="cli")
    store.revoke(suppression_id, actor="cli")
'''

#: A private ledger: satisfies "remembered", fails "until the decline is revoked".
EVASIVE_DECISION_STORE = '''
class _Ledger:
    def record(self, row):
        ...

    def revoke(self, row):
        ...


def run(rows):
    ledger = _Ledger()
    for row in rows:
        ledger.record(row)
        ledger.revoke(row)
'''


def test_the_countdown_bites_the_evasion_that_satisfied_the_name_match():
    """P7's first half, run against the thing the guard exists to catch."""
    assert not calls_review(EVASION_SOURCE, "offer"), (
        "an unrelated method called offer answers for the queue"
    )
    assert not offers_into(EVASION_SOURCE, "Queue.VERSION_MATCH"), (
        "a queue constant reaching no call counts as offering into it"
    )
    assert constructs_a_csv_writer(EVASION_SOURCE), (
        "a comma separated writer behind an aliased import is invisible"
    )
    assert not methods_on_review_construction(EVASIVE_DECISION_STORE, "DecisionStore"), (
        "a private ledger named record and revoke answers for the decision stores (R35)"
    )


@pytest.mark.parametrize(
    "source", [CORRECT_OFFER_MODULE_IMPORT, CORRECT_OFFER_SYMBOL_IMPORT]
)
def test_the_countdown_stays_quiet_on_correct_code_in_either_import_shape(source):
    """P7's second half: a guard that fires on correct code gets routed around."""
    assert calls_review(source, "offer")
    assert offers_into(source, "Queue.VERSION_MATCH")
    assert not constructs_a_csv_writer(source)


@pytest.mark.parametrize(
    "source",
    [
        CORRECT_OFFER_SIBLING_RELATIVE_IMPORT,
        CORRECT_OFFER_SIBLING_BOUND_AS_A_MODULE,
        CORRECT_OFFER_RELATIVE_IMPORT_TWO_LEVELS_UP,
    ],
)
def test_the_countdown_reads_every_relative_import_shape(source):
    """``node.module`` holds only the tail, so the fallback has to read all three spellings."""
    assert calls_review(source, "offer")
    assert offers_into(source, "Queue.VERSION_MATCH")


@pytest.mark.parametrize(
    "source",
    [
        CORRECT_OFFER_SIBLING_RELATIVE_IMPORT,
        CORRECT_OFFER_SIBLING_BOUND_AS_A_MODULE,
    ],
)
def test_a_relative_import_is_resolved_against_the_package_the_file_sits_in(source):
    """``from . import review`` names a different module in ``cratekit.intake`` than in ``cratekit.core``."""
    assert calls_review(source, "offer", "cratekit.core")
    assert offers_into(source, "Queue.VERSION_MATCH", "cratekit.core")
    assert not calls_review(source, "offer", "cratekit.intake"), (
        "a sibling called review in another package answers for cratekit.core.review"
    )
    assert not offers_into(source, "Queue.VERSION_MATCH", "cratekit.intake")
    assert not calls_review(
        EVASION_A_DIFFERENT_SIBLING_CALLED_REVIEW, "offer", "cratekit.intake"
    )
    assert calls_review(
        EVASION_A_DIFFERENT_SIBLING_CALLED_REVIEW, "offer", "cratekit.core"
    ), "the same text one package over IS the review module, so the text is not the question"


def test_the_review_module_is_named_once(monkeypatch):
    """The leaf is derived from ``REVIEW_MODULE``, so moving the constant moves the binding."""
    monkeypatch.setattr(_guards, "REVIEW_MODULE", "cratekit.core.adjudication")
    moved = '''
from cratekit.core import adjudication


def run(store, needing_review):
    for candidate in needing_review:
        adjudication.offer(
            store,
            queue=adjudication.Queue.VERSION_MATCH,
            identity=candidate.identity,
        )
'''
    assert calls_review(moved, "offer")
    assert offers_into(moved, "Queue.VERSION_MATCH")
    assert not calls_review(CORRECT_OFFER_MODULE_IMPORT, "offer"), (
        "the module moved and the binding did not follow it"
    )


def test_the_countdown_reads_a_decision_store_through_a_relative_import():
    """``methods_on_review_construction`` shares the walk, so it shares the defect."""
    source = '''
from .review import DecisionStore


def run(cfg, identity):
    store = DecisionStore("declines", cfg)
    store.record(kind="version", identity=identity, actor="cli")
    store.revoke(identity, actor="cli")
'''
    assert methods_on_review_construction(source, "DecisionStore") >= {
        "record",
        "revoke",
    }
    assert (
        methods_on_review_construction(source, "DecisionStore", "cratekit.intake")
        == set()
    )


@pytest.mark.parametrize(
    "source", [CORRECT_DECISION_STORE, CORRECT_DECISION_STORE_VIA_HELPER]
)
def test_the_decision_store_countdown_stays_quiet_on_correct_code(source):
    assert methods_on_review_construction(source, "DecisionStore") >= {"record", "revoke"}


# The countdowns themselves

#: Every adjudication surface with NO legacy file, and its producing import target (P5):
#: a countdown while pending, and once landed it must offer into its queue.
NEW_SURFACE_OWED_BY: dict[str, str] = {
    review.Queue.DUPLICATES: "cratekit.modules.reports",
    review.Queue.DELETION: "cratekit.deletion",
    review.Queue.ADOPTION: "cratekit.adopt",
    review.Queue.PATH_REPAIR: "cratekit.intake",
}


def test_every_new_adjudication_surface_is_owed_by_a_registered_unit():
    """DERIVED from the split; a landed target is held to producing, so landing cannot switch it off."""
    declared = {
        surface.queue
        for surface in review.SURFACES
        if surface.adjudicated and not surface.legacy_file
    }
    assert set(NEW_SURFACE_OWED_BY) == declared, (
        f"unregistered: {sorted(declared - set(NEW_SURFACE_OWED_BY))}; stale: {sorted(set(NEW_SURFACE_OWED_BY) - declared)}"
    )
    for queue, key in NEW_SURFACE_OWED_BY.items():
        if key in _pending.PENDING:
            continue
        assert not _pending._is_absent(key), (
            f"{queue}: {key} is neither pending nor present, so nothing produces it"
        )
        constant = f"Queue.{review.Queue(queue).name}"
        assert _target_offers_into(key, constant), (
            f"{key} has landed and nothing in it offers into {constant}"
        )


def _target_offers_into(target: str, queue: str) -> bool:
    """Whether ANY module of a landed package, or a single landed module, offers into ``queue`` (P3, P7)."""
    parts = target.split(".")
    root = SRC_ROOT.joinpath(*parts)
    if root.is_dir():
        return any(offers_into(source, queue) for _name, source in package_modules(root))
    single = SRC_ROOT.joinpath(*parts[:-1], f"{parts[-1]}.py")
    return single.is_file() and offers_into(single.read_text(), queue)


@pytest.mark.parametrize(
    "target, expected",
    [
        ("cratekit.modules.reports", True),
        ("cratekit.write", False),
        ("cratekit.modules.reports.duplicates", True),
        ("cratekit.modules.reports.aging", False),
        ("cratekit.modules.reports.no_such_producer", False),
        ("cratekit.nowhere.at_all", False),
    ],
    ids=[
        "package-offers",
        "package-does-not",
        "module-offers",
        "module-does-not",
        "absent-module",
        "absent-package",
    ],
)
def test_a_landed_target_that_does_not_produce_is_not_taken_for_one(target, expected):
    """The helper the landed branch rests on must be able to say no, and False for an absent target."""
    assert _target_offers_into(target, "Queue.DUPLICATES") is expected


def test_the_countdown_can_tell_a_landed_target_from_one_that_is_not_there():
    """``_is_absent`` decides whether an entry off the register landed or never existed."""
    assert not _pending._is_absent("cratekit.modules.reports")
    assert _pending._is_absent("cratekit.modules.reports.no_such_producer")


def test_the_match_verb_sends_only_the_middle_state_to_the_queue():
    """U11's obligation on U16, ARMED. The static half; tests/test_match_states.py is the behavioural one."""
    source = (SRC_ROOT / "cratekit" / "acquire" / "match_cli.py").read_text()
    assert calls_review(source, "offer"), "the match verb never calls this module's offer"
    assert offers_into(source, "Queue.VERSION_MATCH"), (
        "the match verb does not offer into the version match queue (R11)"
    )
    assert not constructs_a_csv_writer(source), (
        "the match verb writes a comma separated file for a person to edit (R12)"
    )


def _package_answers(root: Path) -> tuple[bool, set[str], bool]:
    """The deletion countdown's three questions over a package, as the UNIT is the subject (P3)."""
    modules = package_modules(root)
    reached: set[str] = set()
    for _name, source in modules:
        reached |= methods_on_review_construction(source, "DecisionStore")
    return (
        any(constructs_review(source, "DecisionStore") for _name, source in modules),
        reached,
        any(offers_into(source, "Queue.DELETION") for _name, source in modules),
    )


def test_the_deletion_pass_records_declines_and_tombstones_where_they_are_revocable():
    """U24's obligation, ARMED: R35 and R36 require revocability, walked over the whole package."""
    root = SRC_ROOT / "cratekit" / "deletion"
    constructs, reached, offers = _package_answers(root)
    assert constructs, "the deletion pass does not reach the decision stores at all"
    assert "record" in reached, (
        "the deletion pass never records through a store built from this module (R35)"
    )
    assert "revoke" in reached, "the deletion pass offers no way to revoke a suppression (R36)"
    assert offers, "the deletion pass does not offer into the deletion queue (R35)"
    for name, source in package_modules(root):
        assert not constructs_a_csv_writer(source), (
            f"{name} writes a comma separated file for a person to edit"
        )


#: Everything the countdown asks, SPLIT ACROSS TWO MODULES, the landed shape (P7).
_CORRECT_SPLIT_PACKAGE = {
    "stores.py": """
from cratekit.core import review


def tombstones(cfg):
    return review.DecisionStore("tombstones", cfg)


def record(cfg, identity):
    store = tombstones(cfg)
    return store.record(kind="version", identity=identity, actor="cli")


def undo(cfg, suppression_id):
    store = tombstones(cfg)
    return store.revoke(suppression_id, actor="cli")
""",
    "run.py": """
from cratekit.core import review


def present(store, identity):
    return review.offer(
        store, queue=review.Queue.DELETION, kind="removed-file",
        identity=identity, payload={},
    )
""",
}

#: The same package with a private ledger and another queue; every name still matches.
_EVASIVE_SPLIT_PACKAGE = {
    "stores.py": """
class _Ledger:
    def record(self, row):
        ...

    def revoke(self, row):
        ...


def keep(rows):
    ledger = _Ledger()
    for row in rows:
        ledger.record(row)
        ledger.revoke(row)
""",
    "run.py": """
from cratekit.core import review


def present(store, identity):
    return review.offer(
        store, queue=review.Queue.GENRE, kind="removed-file",
        identity=identity, payload={},
    )
""",
}


def _assemble(root: Path, files: dict[str, str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "__init__.py").write_text("")
    for name, source in files.items():
        (root / name).write_text(source)
    return root


def test_the_deletion_countdown_bites_a_package_that_evades_it(tmp_path):
    """P7's first half, on the guard's own shape rather than on one file's."""
    constructs, reached, offers = _package_answers(
        _assemble(tmp_path / "evasive", _EVASIVE_SPLIT_PACKAGE)
    )
    assert not constructs, (
        "a private ledger named record and revoke answers for the decision stores (R35)"
    )
    assert reached == set()
    assert not offers, "offering into another queue satisfies the deletion countdown (R35)"


def test_the_deletion_countdown_stays_quiet_on_a_correct_package(tmp_path):
    """P7's second half: store access and queue access split across two modules."""
    constructs, reached, offers = _package_answers(
        _assemble(tmp_path / "correct", _CORRECT_SPLIT_PACKAGE)
    )
    assert constructs
    assert {"record", "revoke"} <= reached
    assert offers


def test_the_duplicate_audit_offers_its_pairs_into_the_duplicates_queue():
    """U34's obligation, half of R26, ARMED: the persistent ignore IS a verdict in this queue."""
    assert _target_offers_into("cratekit.modules.reports", "Queue.DUPLICATES")


def test_the_adoption_plan_becomes_review_items_rather_than_a_file():
    """U23's obligation, ARMED (R26): a shape check (P3); the behaviour is in test_adoption."""
    assert _target_offers_into("cratekit.adopt", "Queue.ADOPTION")
    offenders: list[str] = []
    for name, source in package_modules(SRC_ROOT / "cratekit" / "adopt"):
        if constructs_a_csv_writer(source):
            offenders.append(name)
    assert not offenders, (
        f"the adoption package writes a comma separated file to edit: {offenders} (R12)"
    )


def test_the_path_repair_pass_offers_its_proposals_into_the_path_repair_queue():
    """U37's obligation: a proposal is never applied without a decision taken in the queue."""
    assert _target_offers_into("cratekit.intake", "Queue.PATH_REPAIR")



def _hold_one(store):
    review.hold(store, queue=review.Queue.LABEL_RELEASE, kind="label-release",
                identity={"release_id": "r1"}, payload={}, group="g", name="L", reason="r",
                detail={}, run_id="run-1")


def _import_over_a_verdict(store):
    document = review.export_document(store)
    review.resolve(store, document["items"][0]["id"], review.Verdict.ACCEPTED,
                   option="opt-accept", actor="a")
    return lambda: review.import_document(store, document, actor="importer")


@pytest.mark.parametrize(
    ("name", "ready"),
    [
        ("item_id_for", lambda store: lambda: _hold_one(store)),
        ("list_items", lambda store: lambda: review.grouped(
            store, queue=review.Queue.LABEL_RELEASE, by="label")),
        ("_item_from_row", lambda store: (_offer_one(store), _import_over_a_verdict(store))[1]),
    ],
    ids=["hold", "grouped", "import_document"],
)
def test_a_name_patched_on_review_reaches_the_module_it_moved_to(store, monkeypatch, name, ready):
    """U301. hold, grouped and import_document read these through ``core.review``."""
    act = ready(store)
    calls = []
    real = getattr(review, name)
    monkeypatch.setattr(review, name, lambda *a, **k: calls.append(1) or real(*a, **k))
    act()
    assert calls


def test_an_item_a_document_carries_twice_is_applied_once(tmp_path, cfg, store):
    """U301. Inserted open, then resolved by its second entry: one change, not two."""
    item = _offer_one(store, key="twice")
    entry = item.to_json()
    document = _document(entry, {**entry, "verdict": str(review.Verdict.ACCEPTED),
                                 "option": "opt-accept", "actor": "other"})
    with review.open_store(cfg, path=tmp_path / "other" / "queue.db") as receiving:
        result = review.import_document(receiving, document, actor="importer")
    assert result.inserted == (item.item_id,) and result.resolved == (item.item_id,)
    assert result.applied == (item.item_id,)
