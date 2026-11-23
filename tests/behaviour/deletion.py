"""Deletion's scenarios: the review, its confirm gate, the Trash and the tombstones (U310).

`crate delete review` reads the collection, offers every removed row whose
file it can prove is the one the row described and nothing else claims, and
stops at its explicit confirm gate; once the gate is answered it trashes the
confirmed files, records a tombstone per file and moves the watermark.
`crate tombstone list` reads those records back and lifts one. On the
deletion suite's own disposable database, whose two collection rows each
scenario edits with the suite's own raw writer, and the suite's fake Trash
under the scenario's home.

Beside the files the pass takes, each refusal it makes with nothing removed:
a file a playlist still holds, a row with nothing to identify it by, a
decision whose plan digest moved under it, and a tombstone that could not be
written, which puts the file back.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from cratekit.core import rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.deletion import library, watermark
from tests.test_deletion import (
    ONE,
    TWO,
    _fake_trash,
    _history,
    _music,
    _tombstone_store_that_will_not_write,
    _write_rows,
)
from tests.test_deletion import cfg as cfg  # noqa: PLC0414
from tests.test_deletion import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_deletion import library_root as library_root  # noqa: PLC0414
from tests.test_deletion import review_cli as review_cli  # noqa: PLC0414

OK = int(ExitCode.OK)
REFUSED = int(ExitCode.DECISION_REQUIRED)
VERB = ("delete", "review")
GATE = "delete.review.confirm"
#: A title carrying a featured credit, so its tombstone gains the uncredited
#: companion a provider's spelling is matched against (R-431).
CREDITED = "First Track (feat. A Guest)"


def _removed(cfg, *rows: tuple[str, str, str], after: int = 40) -> dict[str, Path]:
    """Mark the disposable database's rows removed after the baseline, one file each.

    Each row is a content id, a file name and a title. The update sequence is
    past ``after``, the baseline's, so the next review offers what it can prove.
    """
    made: dict[str, Path] = {}
    written = []
    for usn, (content_id, name, title) in enumerate(rows, start=after + 10):
        music = _music(cfg, name)
        made[content_id] = music
        written.append((content_id, str(music), True, usn, music.stat().st_size, title))
    _write_rows(Path(cfg.library.db_path), written)
    return made


def _refused(stage) -> dict:
    """The review meeting its confirm gate with nothing recorded, as the envelope."""
    ran = stage.json(*VERB)
    assert ran.code == REFUSED, ran.stdout
    return ran.envelope


def _baselined(cfg) -> None:
    """The watermark a first run leaves, at sequence 40, as the suite's own trash test takes it."""
    handle = rb_writer.open_db(Path(cfg.library.db_path), unlock=False, cfg=cfg)
    try:
        watermark.WatermarkStore(cfg).baseline(
            database_identity=library.database_identity(handle), sequence=40, actor="cli"
        )
    finally:
        rb_writer.close_db(handle)


def _membership(cfg, content_id: str) -> None:
    """A live playlist entry on ``content_id``, as rekordbox leaves one behind.

    Written as a row with plain SQL, as the suite's own ``_write_rows`` edits
    the collection: a membership is exactly what this unit never writes.
    """
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
            "rb_local_deleted) VALUES ('held', '900', ?, 1, 0)",
            (content_id,),
        )
        conn.commit()
    finally:
        conn.close()


def test_review_offers_declines_trashes_and_lists_tombstones(
    stage, review_cli, tmp_path, monkeypatch
):
    _fake_trash(tmp_path, monkeypatch)
    _baselined(review_cli)
    _removed(review_cli, ("1", ONE, CREDITED), ("2", TWO, Path(TWO).stem))

    # The offer as a person reads it, then as the envelope the two acts answer.
    assert stage.crate(*VERB).code == REFUSED
    envelope = _refused(stage)
    assert envelope["cause"]["detail"]["shown"]["offered"] == 2, envelope
    run_id = envelope["run_id"]

    # Every offered file with its proof, then one of them declined by a person.
    listed = stage.json("review", "list", "--queue", "deletion")
    assert listed.code == OK, listed.stdout
    paths = {}
    for item in listed.envelope["data"]["items"]:
        shown = stage.json("review", "show", item["id"])
        assert shown.code == OK, shown.stdout
        (record,) = shown.envelope["data"]["items"]
        paths[record["payload"]["path"]] = item["id"]
    declined = paths[str(Path(review_cli.library.root) / "Music" / TWO)]
    assert stage.crate("review", "resolve", declined, "--verdict", "rejected").code == OK

    # The decline does not move the digest: the gate's plan is the deletable set.
    assert stage.decide(run_id, GATE, "trash").code == OK
    trashed = stage.json("--run", run_id, *VERB)
    assert trashed.code == OK, trashed.stdout

    assert stage.crate("tombstone", "list").code == OK
    listing = stage.json("tombstone", "list")
    assert listing.code == OK, listing.stdout
    held = [item["id"] for item in listing.envelope["data"]["items"]]
    assert held, listing.stdout
    assert stage.json("tombstone", "list", "--revoke", held[0]).code == OK
    assert stage.json("tombstone", "list").code == OK
    assert stage.json("tombstone", "list", "--all").code == OK
    assert stage.crate("tombstone", "list", "--all").code == OK
    # An identifier that resolves in neither store.
    assert stage.json("tombstone", "list", "--revoke", "dc_nope").code != OK


def test_review_aborted_at_the_gate_moves_nothing(stage, review_cli, tmp_path, monkeypatch):
    _fake_trash(tmp_path, monkeypatch)
    _history(review_cli)

    # A first run over history baselines and says so beside the question.
    assert stage.crate(*VERB).code == REFUSED
    envelope = _refused(stage)
    assert stage.decide(envelope["run_id"], GATE, "abort").code == OK
    aborted = stage.json("--run", envelope["run_id"], *VERB)
    assert aborted.code == OK, aborted.stdout
    assert aborted.envelope["outcome"] == "no_op", aborted.stdout

    # Past the counter the first run baselined at, the disposable database's own.
    _removed(review_cli, ("2", TWO, Path(TWO).stem), after=100)
    envelope = _refused(stage)
    assert envelope["cause"]["detail"]["shown"]["offered"] == 1, envelope
    assert stage.decide(envelope["run_id"], GATE, "abort").code == OK
    assert stage.crate("--run", envelope["run_id"], *VERB).code == OK


def test_review_refuses_a_held_file_and_an_unidentifiable_row(
    stage, review_cli, tmp_path, monkeypatch
):
    _fake_trash(tmp_path, monkeypatch)
    _baselined(review_cli)
    # A file a playlist still holds, and a row with no artist and no title.
    _removed(review_cli, ("1", ONE, Path(ONE).stem), ("2", TWO, ""))
    _membership(review_cli, "1")

    envelope = _refused(stage)
    assert envelope["cause"]["detail"]["shown"]["offered"] == 0, envelope
    assert stage.decide(envelope["run_id"], GATE, "trash").code == OK
    assert stage.json("--run", envelope["run_id"], *VERB).code == OK
    assert stage.json("review", "list", "--queue", "deletion").code == OK
    assert stage.json("tombstone", "list", "--all").code == OK


def test_review_refuses_a_decision_whose_digest_moved(stage, review_cli, tmp_path, monkeypatch):
    _fake_trash(tmp_path, monkeypatch)
    _baselined(review_cli)
    made = _removed(review_cli, ("1", ONE, Path(ONE).stem))

    envelope = _refused(stage)
    assert envelope["cause"]["detail"]["shown"]["offered"] == 1, envelope
    assert stage.decide(envelope["run_id"], GATE, "trash").code == OK
    # The file grows after the decision, so the size the row recorded no
    # longer proves it and the plan the person confirmed is not this one.
    with made["1"].open("ab") as grown:
        grown.write(b" and more")
    moved = stage.json("--run", envelope["run_id"], *VERB)
    assert moved.code == int(ExitCode.DECISION_STALE), moved.stdout
    assert stage.json("tombstone", "list", "--all").code == OK


def test_review_puts_the_file_back_when_its_tombstone_cannot_be_written(
    stage, review_cli, tmp_path, monkeypatch
):
    _fake_trash(tmp_path, monkeypatch)
    _baselined(review_cli)
    _removed(review_cli, ("1", ONE, Path(ONE).stem))

    envelope = _refused(stage)
    run_id = envelope["run_id"]
    assert stage.decide(run_id, GATE, "trash").code == OK
    broken = _tombstone_store_that_will_not_write(monkeypatch)
    failed = stage.json("--run", run_id, *VERB)
    assert failed.code not in (OK, REFUSED), failed.stdout
    assert stage.json("tombstone", "list", "--all").code == OK

    # With the store writable again the same decision finishes the deletion.
    broken["on"] = False
    assert stage.json("--run", run_id, *VERB).code == OK
    assert stage.json("tombstone", "list").code == OK
