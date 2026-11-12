"""U243: a rekordbox streaming row is not a local file, and an unmapped one is named.

The live ``crate delete review`` that filed this card refused on 153 active rows
"this machine cannot resolve". Read from the database, 137 of them were
rekordbox streaming rows recorded as ``/v4/catalog/tracks/<id>/``, which starts
with a slash and so reaches the resolver as a path nothing maps, and 16 were old
laptop paths. A streaming row can name no local file, yet it held every deletion.

What must stay true is the half that protects music: a row that COULD name a
real file still refuses, so the excusal is the exact streaming spelling, with
nothing at it on this machine, and every other unmapped row refuses as before,
now named by its prefix with the rule that would resolve it.

D1 applies. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from cratekit.core import locations, rb_writer
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.deletion import candidates, library, stores, watermark
from cratekit.write import trees
from tests.test_deletion import (
    ONE,
    _categorize,
    _drive,
    _fake_trash,
    _music,
    _references,
    _removed,
    _write_rows,
)
from tests.test_deletion import cfg as cfg  # noqa: PLC0414 - fixture
from tests.test_deletion import gates_pass as gates_pass  # noqa: PLC0414 - fixture
from tests.test_deletion import library_root as library_root  # noqa: PLC0414 - fixture
from tests.test_deletion import review_cli as review_cli  # noqa: PLC0414 - fixture

STREAMED = (
    "/v4/catalog/tracks/12345678/",
    "/v4/catalog/tracks/87654321",
    "/v4/catalog/tracks/AbC9/",
)


def _active(*recorded: str) -> list[trees.ContentRow]:
    return [
        trees.ContentRow(content_id=f"a{index}", recorded=value, deleted=False)
        for index, value in enumerate(recorded)
    ]


def _absent(path):
    raise FileNotFoundError(path)


# ═══════════════════════════════════════════════════════════════════════════
# 1. The reference set
# ═══════════════════════════════════════════════════════════════════════════


def test_a_library_with_streaming_rows_offers_the_removed_file(cfg):
    """The defect, as the live library had it: streaming rows held every deletion."""
    _music(cfg, ONE)
    references = _references(cfg, _active(*STREAMED, "soundcloud:tracks:42"))
    assert references.unmapped == ()
    assert references.streaming == ("a0", "a1", "a2")
    assert references.not_a_path == ("a3",)
    assert references.ignored == 4
    assert references.counts["streaming"] == 3
    assert references.complete
    candidates.assert_complete(references)
    answered = _categorize(cfg, [_removed(cfg, ONE, "1")], references)
    assert answered[0].category is candidates.Category.DELETABLE


@pytest.mark.parametrize(
    "recorded",
    [
        "/v4/catalog/tracks/123/track.flac",
        "/v4/catalog/tracks/123.flac/",
        "/v4/catalog/tracks/12_3/",
        "/V4/catalog/tracks/123/",
        "/v4//catalog/tracks/123/",
        "/v4/catalog/tracks//",
        "/v4/catalog/tracks/",
        "/v4/catalog/albums/123/",
        "/v5/catalog/tracks/123/",
        "/Elsewhere/v4/catalog/tracks/123/",
        "/v4/catalog/tracks/123/\n",
    ],
)
def test_a_path_shaped_only_near_a_streaming_row_still_refuses(cfg, recorded):
    """Only the exact spelling is excused: anything else could be a real path."""
    references = _references(cfg, _active(recorded), stat=_absent)
    assert references.streaming == ()
    assert references.unmapped == ("a0",)
    assert not references.complete
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    assert excinfo.value.cause.reason == "deletion-reference-set-incomplete"


@pytest.mark.parametrize(
    "answer", [None, PermissionError("no"), NotADirectoryError("no"), ValueError("nul")]
)
def test_a_streaming_spelling_with_anything_at_it_still_refuses(cfg, answer):
    """FAILS CLOSED: something there, or a question the filesystem would not answer."""

    def stat(path):
        if answer is None:
            return Path(cfg.library.root).stat()
        raise answer

    references = _references(cfg, _active(STREAMED[0]), stat=stat)
    assert references.streaming == ()
    assert references.unmapped == ("a0",)
    with pytest.raises(CratekitError):
        candidates.assert_complete(references)


def test_a_streaming_spelling_is_asked_about_on_the_disk(cfg):
    """The stat is asked at the recorded spelling, not assumed."""
    asked: list[str] = []

    def stat(path):
        asked.append(str(path))
        raise FileNotFoundError(path)

    _references(cfg, _active(STREAMED[0]), stat=stat)
    assert asked == [STREAMED[0]]


def test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule(cfg):
    references = _references(
        cfg,
        _active(
            "/Users/someone/Music/a.flac",
            "/Users/someone/Music/b.flac",
            "/Old Drive/Music/c.flac",
            STREAMED[0],
        ),
        stat=_absent,
    )
    assert references.streaming == ("a3",)
    assert references.unmapped == ("a0", "a1", "a2")
    assert references.unmapped_prefixes == (("/Users/someone", 2), ("/Old Drive/Music", 1))
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    cause = excinfo.value.cause
    assert cause.reason == "deletion-reference-set-incomplete"
    assert "3 active rows record a location this machine cannot resolve" in cause.message
    assert "2 under /Users/someone" in cause.message
    assert "1 under /Old Drive/Music" in cause.message
    steps = " ".join(cause.remediation.steps)
    # ONE ENTRY TO ADD TO THE LIST, never a second assignment of the key, which
    # a configuration already holding a rule refuses to load.
    assert "to the library.location_prefix_map list" in steps
    assert "location_prefix_map = [" not in steps
    assert 'from = "/Users/someone"' in steps
    assert 'from = "/Old Drive/Music"' in steps
    assert cause.detail["unmapped_prefixes"] == {"/Users/someone": 2, "/Old Drive/Music": 1}
    assert cause.detail["streaming"] == 1


def test_a_refusal_names_at_most_five_prefixes_and_counts_the_rest(cfg):
    rows = _active(*(f"/Drive{n}/Music/x.flac" for n in range(7)))
    references = _references(cfg, rows, stat=_absent)
    with pytest.raises(CratekitError) as excinfo:
        candidates.assert_complete(references)
    message = excinfo.value.cause.message
    assert "and 2 other prefixes" in message
    assert message.count(" under /Drive") == 5


# ═══════════════════════════════════════════════════════════════════════════
# 2. Through the shipped verb, on a disposable database
# ═══════════════════════════════════════════════════════════════════════════


def _insert_active(db_path: Path, rows: list[tuple[str, str]]) -> None:
    """Active collection rows written with raw SQL, as ``_write_rows`` writes."""
    conn = sqlite3.connect(db_path)
    try:
        for content_id, recorded in rows:
            conn.execute(
                "INSERT INTO djmdContent (ID, FolderPath, rb_local_deleted, rb_local_usn, "
                "Title) VALUES (?, ?, 0, 20, ?)",
                (content_id, recorded, f"Streamed {content_id}"),
            )
        conn.commit()
    finally:
        conn.close()


def test_delete_review_trashes_a_removed_file_beside_streaming_rows(
    review_cli, tmp_path, monkeypatch
):
    """The card's scenario end to end: the verb that refused now finishes."""
    trash = _fake_trash(tmp_path, monkeypatch)
    music = _music(review_cli, ONE)
    db_path = Path(review_cli.library.db_path)
    handle = rb_writer.open_db(db_path, unlock=False, cfg=review_cli)
    try:
        watermark.WatermarkStore(review_cli).baseline(
            database_identity=library.database_identity(handle),
            sequence=40,
            actor="cli",
        )
    finally:
        rb_writer.close_db(handle)
    _write_rows(
        db_path,
        [
            ("1", str(music), True, 50, music.stat().st_size, Path(ONE).stem),
            ("2", "/v4/catalog/tracks/11111111/", False, 20, 0, "Streamed 2"),
        ],
    )
    _insert_active(
        db_path, [("3", "/v4/catalog/tracks/22222222/"), ("4", "soundcloud:tracks:33")]
    )

    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code == int(ExitCode.DECISION_REQUIRED), err or out
    refused = json.loads(out)
    assert refused["cause"]["detail"]["shown"]["ignored, not local files"] == 3
    assert refused["cause"]["detail"]["shown"]["offered"] == 1
    run_id = refused["run_id"]
    code, _, err = _drive(
        ["run", "decide", run_id, "delete.review.confirm", "trash", "--actor", "a-person"]
    )
    assert code == int(ExitCode.OK), err
    code, out, err = _drive(["--output", "json", "--run", run_id, "delete", "review"])
    assert code == int(ExitCode.OK), err or out
    # WHERE THE TRASH IS belongs to the platform, and the Trash tests own it;
    # what this card owes is that the verb finished: the file was moved and its
    # removal recorded with where it went.
    del trash
    assert not music.exists()
    (recorded,) = stores.list_tombstones(review_cli)
    assert recorded.payload["trashed_to"]


def test_delete_review_still_refuses_an_unmapped_local_row_beside_streaming_rows(
    review_cli, tmp_path, monkeypatch
):
    trash = _fake_trash(tmp_path, monkeypatch)
    music = _music(review_cli, ONE)
    db_path = Path(review_cli.library.db_path)
    handle = rb_writer.open_db(db_path, unlock=False, cfg=review_cli)
    try:
        watermark.WatermarkStore(review_cli).baseline(
            database_identity=library.database_identity(handle),
            sequence=40,
            actor="cli",
        )
    finally:
        rb_writer.close_db(handle)
    _write_rows(
        db_path,
        [
            ("1", str(music), True, 50, music.stat().st_size, Path(ONE).stem),
            ("2", "/v4/catalog/tracks/11111111/", False, 20, 0, "Streamed 2"),
        ],
    )
    _insert_active(db_path, [("3", "/A Retired Drive/Music/x.flac")])

    code, out, err = _drive(["--output", "json", "delete", "review"])
    assert code != int(ExitCode.OK)
    refused = json.loads(out)
    assert refused["cause"]["reason"] == "deletion-reference-set-incomplete"
    assert "1 under /A Retired Drive/Music" in refused["cause"]["message"]
    assert music.exists() and not any(trash.iterdir())


def test_a_rule_a_person_wrote_over_the_streaming_spelling_wins(cfg):
    """Configuration wins: the row resolves through the rule and is indexed."""
    target = Path(cfg.library.root) / "Music" / "tracks" / "123"
    target.mkdir(parents=True)
    rule = locations.PrefixRule("/v4/catalog", str(Path(cfg.library.root) / "Music"))
    references = _references(cfg, _active("/v4/catalog/tracks/123/"), prefix_map=[rule])
    assert references.streaming == ()
    assert references.unmapped == ()
    assert len(references.by_identity) == 1
