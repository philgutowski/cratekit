"""The review queue's scenarios: offered, grouped, resolved, withheld, exported and imported (U301).

Items are offered and a label release withheld through the store, as a
producer files them, then every `crate review` verb reads and writes them, so
the capture holds the queue's database and each export file the verbs leave.
On the review queue suite's own configured library.
"""

from __future__ import annotations

from cratekit.core import review
from cratekit.core.exit_codes import ExitCode
from tests.test_review_queue import cfg as cfg  # noqa: PLC0414

OK = int(ExitCode.OK)
VERSION = "version-difference"


def _offer(store, key: str) -> review.Item:
    return review.offer(
        store,
        queue=review.Queue.VERSION_MATCH,
        kind=VERSION,
        identity={"source": "list-1", "row": key},
        payload={"wanted": f"track {key}", "found": f"track {key} (edit)", "run_id": "run-1"},
        options=(
            review.Option(option_id="opt-accept", summary="the edit is the same recording"),
            review.Option(option_id="opt-other", summary="a different recording entirely"),
        ),
        handler_key="match.run",
    )


def test_review_queue_offered_resolved_withheld_exported_and_imported(stage, cfg, tmp_path):
    with review.open_store(cfg) as store:
        first, second, third, fourth = (_offer(store, key) for key in "abcd")
        review.record_round(
            store, queue=review.Queue.VERSION_MATCH, run_id="run-1", group="g", name="G", beyond=2
        )
        review.withhold(
            store,
            fourth.item_id,
            group="g",
            name="G",
            reason="already filed",
            detail={"kind": "dance"},
            run_id="run-1",
        )
    stage.crate("review", "list")
    stage.json("review", "list", "--group-by", "run")
    stage.crate("review", "list", "--group-by", "label")
    stage.crate("review", "show", first.item_id)
    assert stage.json("review", "resolve", first.item_id, "--verdict", "accepted").code == OK
    stage.crate("review", "resolve", second.item_id, "--verdict", "rejected")
    stage.crate("review", "resolve", "--where", f"kind={VERSION}", "--verdict", "superseded")
    stage.json("review", "list", "--all", "--suppressed")
    exported = tmp_path / "queue.json"
    assert stage.crate("review", "export", str(exported)).code == OK
    stage.crate("review", "clear", second.item_id)
    stage.json("review", "import", str(exported))
    stage.crate("review", "list", "--all", "--limit", "2")
    stage.crate("review", "show", third.item_id)
