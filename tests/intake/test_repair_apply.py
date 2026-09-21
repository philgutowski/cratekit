"""U102: ``repair paths --apply`` renames what a person accepted, and only that.

Every test drives the real dispatcher. The proposals are made by the verb's own
scan, the verdicts are recorded through the review store the way ``review
resolve`` records one, and the collection guard is driven against a disposable
database, never a stub, wherever the test is about the guard.

THE EXPECTED NAMES ARE WRITTEN OUT, never read back from the plan, so an
assertion here cannot reduce to the code agreeing with itself.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.core import config, rb_writer, review
from cratekit.core.exit_codes import ExitCode
from cratekit.core.review import Queue, Verdict
from cratekit.intake import repair
from cratekit.write import naming_cli
from tests.test_config import valid_data
from tests.test_naming_apply_cli import _record
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database

#: A name whose trailing segment repeats its lead, and what the scan proposes.
LONG = "04A - 124 - Song - Artist - Song.flac"
SHORT = "04A - 124 - Song - Artist.flac"
OTHER_LONG = "05A - 120 - Tune - Band - Tune.flac"
OTHER_SHORT = "05A - 120 - Tune - Band.flac"

#: ``repair`` is a feature module, and the slim profile switches its verbs off.
FULL = {"name": "full"}


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library, monkeypatch):
    """A machine whose collection READ and holds no row, which is a real state."""
    resolved = config.from_dict(valid_data(library, profile=FULL))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: ())
    return resolved


@pytest.fixture
def collected(library, monkeypatch):
    """A configured machine whose collection is a real, readable database."""
    from pyrekordbox.db6 import database as binding

    data = valid_data(
        library,
        profile=FULL,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    resolved = config.from_dict(data)
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    _build_disposable_database(Path(resolved.library.db_path), with_tag_category=False)
    return resolved


def drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def _folder(cfg) -> Path:
    folder = Path(cfg.library.root) / "Music" / "wave"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _audio(folder: Path, name: str, body: bytes = b"fLaC") -> Path:
    path = folder / name
    path.write_bytes(body)
    return path


def _scan(folder: Path) -> dict:
    code, out, _ = drive(["--output", "json", "repair", "paths", "--root", str(folder)])
    assert code == int(ExitCode.OK), out
    return json.loads(out)["data"]


def _decide(cfg, path: Path, verdict: Verdict | None, option: str | None = None) -> None:
    """Record a verdict on the one item offered for ``path``, as a person would."""
    wanted = review.item_id_for(
        str(Queue.PATH_REPAIR), repair.KIND, {"path": str(path.resolve())}
    )
    with review.open_store(cfg) as store:
        assert review.find(store, wanted) is not None, "the scan offered no item for it"
        if verdict is not None:
            review.resolve(store, wanted, verdict, option=option, actor="a-person")


def _accept(cfg, path: Path) -> None:
    _decide(cfg, path, Verdict.ACCEPTED, repair.ACCEPT)


def _answer(option: str, *extra: str) -> tuple[int, dict]:
    code, out, _ = drive([
        "--output", "json", "-d", f"repair.paths.confirm={option}",
        "repair", "paths", "--apply", *extra,
    ])
    return code, json.loads(out)


def _actions(plan: dict) -> dict[str, str]:
    return {item["from"]: item["action"] for item in plan["items"]}


def _names(folder: Path) -> set[str]:
    return {path.name for path in folder.iterdir()}


# ---------------------------------------------------------------------------
# The brief's four scenarios
# ---------------------------------------------------------------------------


def test_an_accepted_proposal_renames_its_file(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG, b"fLaC the audio")
    assert _scan(folder)["items"][0]["proposed"] == SHORT
    _accept(configured, path)

    code, envelope = _answer("apply")

    assert code == int(ExitCode.OK), envelope
    assert _names(folder) == {SHORT}
    assert (folder / SHORT).read_bytes() == b"fLaC the audio"
    totals = envelope["data"]["totals"]
    assert (totals["count"], totals["renamed"], totals["incomplete"]) == (1, 1, 0)


def test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed(collected):
    folder = _folder(collected)
    held = _audio(folder, LONG)
    free = _audio(folder, OTHER_LONG)
    _scan(folder)
    _accept(collected, held)
    _accept(collected, free)
    _record(collected, str(held), identifier="10")

    code, envelope = _answer("apply")

    assert _names(folder) == {LONG, OTHER_SHORT}
    assert _actions(envelope["data"]) == {LONG: "referenced", OTHER_LONG: "rename"}
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "rename-incomplete"
    detail = envelope["cause"]["detail"]
    assert (detail["renamed"], detail["incomplete_count"]) == (1, 1)
    assert detail["incomplete"][0]["from"] == LONG
    assert "collection references it" in detail["incomplete"][0]["why"]


def test_an_open_or_rejected_or_kept_proposal_is_untouched(configured):
    folder = _folder(configured)
    still_open = _audio(folder, LONG)
    rejected = _audio(folder, OTHER_LONG)
    kept = _audio(folder, "06A - 118 - Air - Duo - Air.flac")
    no_option = _audio(folder, "07A - 110 - Sea - Trio - Sea.flac")
    _scan(folder)
    _decide(configured, still_open, None)
    _decide(configured, rejected, Verdict.REJECTED)
    _decide(configured, kept, Verdict.ACCEPTED, repair.KEEP)
    _decide(configured, no_option, Verdict.ACCEPTED, None)
    before = _names(folder)

    code, envelope = _answer("apply")

    assert code == int(ExitCode.OK), envelope
    assert _names(folder) == before
    assert envelope["data"]["items"] == []
    totals = envelope["data"]["totals"]
    assert (totals["open"], totals["rejected"], totals["kept"]) == (1, 1, 2)
    assert (totals["count"], totals["renamed"]) == (0, 0)


def test_a_collision_refuses_that_file_and_names_it(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG, b"fLaC mine")
    free = _audio(folder, OTHER_LONG)
    _scan(folder)
    _accept(configured, path)
    _accept(configured, free)
    # Somebody else's file takes the proposed name after the scan.
    _audio(folder, SHORT, b"fLaC theirs")

    code, envelope = _answer("apply")

    assert (folder / LONG).read_bytes() == b"fLaC mine"
    assert (folder / SHORT).read_bytes() == b"fLaC theirs"
    assert (folder / OTHER_SHORT).is_file()
    assert _actions(envelope["data"]) == {LONG: "collides", OTHER_LONG: "rename"}
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["outcome"] != "ok"
    assert envelope["cause"]["reason"] == "rename-incomplete"
    assert LONG in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["incomplete"][0]["from"] == LONG
    assert SHORT in envelope["cause"]["detail"]["incomplete"][0]["why"]


# ---------------------------------------------------------------------------
# The gate, convergence, and the guards around the rename
# ---------------------------------------------------------------------------


def test_the_gate_refuses_unanswered_and_an_abort_touches_nothing(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)

    code, out, _ = drive(["--output", "json", "repair", "paths", "--apply"])
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert json.loads(out)["cause"]["detail"]["gate"] == "repair.paths.confirm"
    assert _names(folder) == {LONG}

    code, envelope = _answer("abort")
    assert code == int(ExitCode.OK)
    assert envelope["data"]["totals"]["count"] == 1
    assert _names(folder) == {LONG}


def test_without_the_flag_an_accepted_proposal_is_not_applied(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    _scan(folder)
    assert _names(folder) == {LONG}


def test_a_second_apply_reads_the_rename_as_done_and_answers_ok(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    assert _answer("apply")[0] == int(ExitCode.OK)

    code, envelope = _answer("apply")

    assert code == int(ExitCode.OK), envelope
    assert _actions(envelope["data"]) == {LONG: "applied"}
    totals = envelope["data"]["totals"]
    assert (totals["count"], totals["applied"], totals["renamed"]) == (0, 1, 0)
    assert _names(folder) == {SHORT}


def test_an_accepted_file_that_is_gone_is_missing_and_not_called_applied(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    path.unlink()

    code, envelope = _answer("apply")

    assert code == int(ExitCode.OK), envelope
    assert _actions(envelope["data"]) == {LONG: "missing"}
    assert envelope["data"]["totals"]["missing"] == 1
    assert _names(folder) == set()


def test_two_accepted_proposals_for_one_name_rename_neither(configured):
    folder = _folder(configured)
    first = _audio(folder, LONG, b"fLaC one")
    second = _audio(folder, OTHER_LONG, b"fLaC two")
    _scan(folder)
    _accept(configured, first)
    _accept(configured, second)
    # The scan cannot propose one name for two files in one folder, so the
    # second proposal is pointed at the first one's name in the store.
    _rewrite_proposed(configured, second, SHORT)

    code, envelope = _answer("apply")

    assert code == int(ExitCode.PRECONDITION)
    assert _actions(envelope["data"]) == {LONG: "collides", OTHER_LONG: "collides"}
    assert first.read_bytes() == b"fLaC one" and second.read_bytes() == b"fLaC two"
    assert not (folder / SHORT).exists()
    assert envelope["cause"]["detail"]["incomplete_count"] == 2


def test_a_row_that_appears_after_the_gate_holds_the_file(configured, monkeypatch):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    reads = iter([(), (str(path),)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))

    code, envelope = _answer("apply")

    assert _names(folder) == {LONG}
    assert code == int(ExitCode.PRECONDITION)
    assert _actions(envelope["data"]) == {LONG: "rename"}
    assert "after the plan was approved" in envelope["cause"]["detail"]["incomplete"][0]["why"]
    assert envelope["data"]["totals"]["renamed"] == 0


def test_an_unreadable_collection_refuses_and_renames_nothing(configured, monkeypatch):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    monkeypatch.undo()
    # No database was ever built under this library, so the read fails for real.
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(Path(configured.library.root)))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: configured)

    code, envelope = _answer("apply")

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert _names(folder) == {LONG}


def _rewrite_proposed(cfg, path: Path, proposed: str) -> None:
    """Put a name in the stored payload, as an edited import document could."""
    wanted = review.item_id_for(
        str(Queue.PATH_REPAIR), repair.KIND, {"path": str(path.resolve())}
    )
    with review.open_store(cfg) as store:
        payload = dict(review.get(store, wanted).payload)
        payload["proposed"] = proposed
        with store.immediate() as conn:
            conn.execute(
                "UPDATE review_items SET payload = ? WHERE item_id = ?",
                (json.dumps(payload), wanted),
            )


@pytest.mark.parametrize(
    ("proposed", "said"),
    [
        ("../escaped.flac", "not a bare filename"),
        ("nested/inside.flac", "not a bare filename"),
        ("", "not a bare filename"),
        ("04A - 124 - Song - Artist.txt", "change the file's extension"),
    ],
)
def test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied(
    configured, proposed, said
):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    _rewrite_proposed(configured, path, proposed)

    code, envelope = _answer("apply")

    assert _names(folder) == {LONG}
    assert not (folder.parent / "escaped.flac").exists()
    assert _actions(envelope["data"]) == {LONG: "unusable"}
    assert code == int(ExitCode.PRECONDITION)
    assert said in envelope["cause"]["detail"]["incomplete"][0]["why"]


def test_a_root_limits_the_apply_and_counts_what_it_left_out(configured):
    inside = _folder(configured)
    outside = Path(configured.library.root) / "Music" / "other"
    outside.mkdir()
    near = _audio(inside, LONG)
    far = _audio(outside, OTHER_LONG)
    _scan(inside)
    _scan(outside)
    _accept(configured, near)
    _accept(configured, far)

    code, envelope = _answer("apply", "--root", str(inside))

    assert code == int(ExitCode.OK), envelope
    assert _names(inside) == {SHORT}
    assert _names(outside) == {OTHER_LONG}
    assert envelope["data"]["totals"]["outside_root"] == 1


def test_the_decided_reader_reads_accepted_as_verdict_and_option_together(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG)
    _scan(folder)
    _accept(configured, path)
    with review.open_store(configured) as store:
        decided = repair.decided(store)
    assert [(a.path, a.proposed) for a in decided.accepted] == [(str(path.resolve()), SHORT)]
    assert (decided.kept, decided.rejected, decided.still_open) == (0, 0, 0)
