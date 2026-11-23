"""U102: ``repair paths --apply`` renames what a person accepted, and only that.

The real dispatcher, the verb's own scan, verdicts recorded through the review
store, and a disposable database wherever a test is about the collection guard.
THE EXPECTED NAMES ARE WRITTEN OUT, never read back from the plan.
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

#: The collection read, taken at import before ``configured`` stubs it, so a
#: test about the read can put back that one patch and nothing else.
_REAL_RECORDED = naming_cli._recorded


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
    argv = ["--output", "json", "-d", f"repair.paths.confirm={option}", "repair", "paths"]
    code, out, _ = drive([*argv, "--apply", *extra])
    return code, json.loads(out)


def _scan_accept(cfg, folder: Path, *paths: Path) -> None:
    _scan(folder)
    for path in paths:
        _accept(cfg, path)


def _one_accepted(cfg, body: bytes = b"fLaC") -> tuple[Path, Path]:
    """One file named LONG, scanned, its proposal accepted. Answers (folder, file)."""
    folder = _folder(cfg)
    path = _audio(folder, LONG, body)
    _scan_accept(cfg, folder, path)
    return folder, path


def _actions(plan: dict) -> dict[str, str]:
    return {item["from"]: item["action"] for item in plan["items"]}


def _names(folder: Path) -> set[str]:
    return {path.name for path in folder.iterdir()}


def test_an_accepted_proposal_is_shown_asked_renamed_and_then_converges(configured):
    folder = _folder(configured)
    path = _audio(folder, LONG, b"fLaC the audio")
    assert _scan(folder)["items"][0]["proposed"] == SHORT
    _accept(configured, path)
    # THE DECIDED READER READS ACCEPTED AS VERDICT AND OPTION TOGETHER.
    with review.open_store(configured) as store:
        decided = repair.decided(store)
    assert [(a.path, a.proposed) for a in decided.accepted] == [(str(path.resolve()), SHORT)]
    assert (decided.kept, decided.rejected, decided.still_open) == (0, 0, 0)
    # WITHOUT THE FLAG an accepted proposal is not applied.
    _scan(folder)
    assert _names(folder) == {LONG}

    # THE GATE REFUSES UNANSWERED, and an abort touches nothing.
    code, out, _ = drive(["--output", "json", "repair", "paths", "--apply"])
    assert code == int(ExitCode.DECISION_REQUIRED)
    assert json.loads(out)["cause"]["detail"]["gate"] == "repair.paths.confirm"
    assert json.loads(out)["cause"]["detail"]["shown"]["root"] is None
    assert _names(folder) == {LONG}
    code, envelope = _answer("abort")
    assert code == int(ExitCode.OK)
    assert envelope["data"]["totals"]["count"] == 1
    assert _names(folder) == {LONG}

    # THE GATE SHOWS EVERY ITEM THE DIGEST WAS TAKEN OVER (R-693): the items,
    # the digest, the root and the totals, so a person confirms what they read.
    code, out, _ = drive(["--output", "json", "repair", "paths", "--apply", "--root", str(folder)])
    assert code == int(ExitCode.DECISION_REQUIRED), out
    shown = json.loads(out)["cause"]["detail"]["shown"]
    code, declined = _answer("abort", "--root", str(folder))
    assert code == int(ExitCode.OK), declined
    assert shown["items"] == declined["data"]["items"]
    assert shown["items"][0]["from"] == LONG and shown["items"][0]["to"] == SHORT
    assert shown["digest"] == declined["data"]["digest"]
    assert shown["count"] == 1
    totals = declined["data"]["totals"]
    assert shown["renames"] == totals["count"] == 1
    assert "totals" not in shown, "two lines both called count would read as a contradiction"
    for name, value in totals.items():
        if name != "count":
            assert shown[name] == value, name
    assert shown["root"] == str(folder)
    assert _names(folder) == {LONG}

    # APPLIED, the accepted proposal renames its file.
    code, envelope = _answer("apply")
    assert code == int(ExitCode.OK), envelope
    assert _names(folder) == {SHORT}
    assert (folder / SHORT).read_bytes() == b"fLaC the audio"
    totals = envelope["data"]["totals"]
    assert (totals["count"], totals["renamed"], totals["incomplete"]) == (1, 1, 0)

    # A SECOND APPLY CONVERGES and claims only what it observed.
    code, envelope = _answer("apply")
    assert code == int(ExitCode.OK), envelope
    assert _actions(envelope["data"]) == {LONG: "missing"}
    assert "already carried out" in envelope["data"]["items"][0]["why"]
    totals = envelope["data"]["totals"]
    assert (totals["count"], totals["missing"], totals["renamed"]) == (0, 1, 0)
    assert _names(folder) == {SHORT}


def test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan(collected):
    """R-500's guard, through this verb: a row no rule resolves, whose file is
    absent and whose name is one this pass would rename, refuses before any
    rename, in name apply's words, and the plan's own read carries it, so the
    abort answer sees it too. The candidates are this verb's own (R-675)."""
    folder, held = _one_accepted(collected)
    _record(collected, f"/mnt/volume/Music/{LONG}", identifier="10")
    code, envelope = _answer("abort")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "collection-row-unmapped"
    assert _names(folder) == {LONG}
    code, envelope = _answer("apply")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "collection-row-unmapped"
    assert envelope["cause"]["detail"]["could_name"] == [
        {"row": f"/mnt/volume/Music/{LONG}", "files": [str(held)]}
    ]
    assert _names(folder) == {LONG}


def test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename(
    collected, monkeypatch
):
    """The apply's own read, with its own candidates: the plan saw a collection
    every row of which resolved, and the read after the gate finds a dark row
    under the name of the file about to be renamed."""
    folder, held = _one_accepted(collected)
    reads = iter([(), (f"/mnt/volume/Music/{LONG}",)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))
    code, envelope = _answer("apply")
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "collection-row-unmapped"
    assert envelope["cause"]["detail"]["could_name"] == [
        {"row": f"/mnt/volume/Music/{LONG}", "files": [str(held)]}
    ]
    assert _names(folder) == {LONG}


def test_a_dark_row_under_another_name_lets_the_repair_run(collected):
    folder, held = _one_accepted(collected)
    _record(collected, "/mnt/volume/Music/elsewhere.flac", identifier="10")
    code, envelope = _answer("apply")
    assert code == int(ExitCode.OK), envelope
    assert _names(folder) == {SHORT}


def test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed(collected):
    folder = _folder(collected)
    held = _audio(folder, LONG)
    free = _audio(folder, OTHER_LONG)
    _scan_accept(collected, folder, held, free)
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
    # A second run holds the same file, so a driver must not be told to retry.
    assert envelope["cause"]["retryable"] is False


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
    _scan_accept(configured, folder, path, free)
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
    assert envelope["cause"]["retryable"] is True
    assert envelope["cause"]["detail"]["incomplete"][0]["from"] == LONG
    assert SHORT in envelope["cause"]["detail"]["incomplete"][0]["why"]


def test_an_accepted_file_that_is_gone_says_no_file_carries_the_name(configured):
    folder, path = _one_accepted(configured)
    path.unlink()
    code, envelope = _answer("apply")
    assert code == int(ExitCode.OK), envelope
    assert _actions(envelope["data"]) == {LONG: "missing"}
    assert "none carries the proposed name" in envelope["data"]["items"][0]["why"]
    assert envelope["data"]["totals"]["missing"] == 1
    assert _names(folder) == set()


def test_a_proposal_that_asked_for_no_change_is_listed_with_its_reason(configured):
    folder, path = _one_accepted(configured)
    # What a proposal that failed to fit looks like: its own name, and why.
    _rewrite_payload(configured, path, proposed=LONG, error="the path is over budget")
    code, envelope = _answer("apply")
    assert code == int(ExitCode.OK), envelope
    assert _actions(envelope["data"]) == {LONG: "unchanged"}
    assert envelope["data"]["items"][0]["why"] == "the path is over budget"
    assert envelope["data"]["totals"]["unchanged"] == 1
    assert _names(folder) == {LONG}


def test_a_linked_file_is_never_renamed_through_its_link(configured, tmp_path):
    folder = _folder(configured)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    real = _audio(elsewhere, "track01.flac", b"fLaC real")
    link = folder / LONG
    link.symlink_to(real)
    _scan(folder)
    _accept(configured, link)
    code, envelope = _answer("apply")
    assert real.read_bytes() == b"fLaC real"
    assert _names(elsewhere) == {"track01.flac"}
    assert _names(folder) == {LONG}
    assert [item["action"] for item in envelope["data"]["items"]] == ["unusable"]
    assert code == int(ExitCode.PRECONDITION)
    assert "linked file" in envelope["cause"]["detail"]["incomplete"][0]["why"]


def test_an_interrupt_or_a_refused_rename_after_the_claim_leaves_no_stub(
    configured, monkeypatch
):
    folder, path = _one_accepted(configured, b"fLaC mine")

    def interrupted(self, target):
        raise KeyboardInterrupt

    monkeypatch.setattr(Path, "rename", interrupted)
    with pytest.raises(KeyboardInterrupt):
        _answer("apply")
    assert _names(folder) == {LONG}
    assert path.read_bytes() == b"fLaC mine"

    def refused(self, target):  # A REFUSED RENAME is named, and leaves no stub either.
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(Path, "rename", refused)
    code, envelope = _answer("apply")
    assert _names(folder) == {LONG}
    assert code == int(ExitCode.PRECONDITION)
    assert "Permission denied" in envelope["cause"]["detail"]["incomplete"][0]["why"]
    assert envelope["cause"]["retryable"] is True
    assert envelope["data"]["totals"]["renamed"] == 0


def test_two_accepted_proposals_for_one_name_rename_neither(configured):
    folder = _folder(configured)
    first = _audio(folder, LONG, b"fLaC one")
    second = _audio(folder, OTHER_LONG, b"fLaC two")
    _scan_accept(configured, folder, first, second)
    # The scan cannot propose one name for two files in one folder, so the
    # second proposal is pointed at the first one's name in the store.
    _rewrite_proposed(configured, second, SHORT)
    code, envelope = _answer("apply")
    assert code == int(ExitCode.PRECONDITION)
    assert _actions(envelope["data"]) == {LONG: "collides", OTHER_LONG: "collides"}
    assert first.read_bytes() == b"fLaC one" and second.read_bytes() == b"fLaC two"
    assert not (folder / SHORT).exists()
    assert envelope["cause"]["detail"]["incomplete_count"] == 2


def test_a_row_after_the_gate_holds_the_file_and_an_unreadable_collection_refuses(configured, monkeypatch):
    folder, path = _one_accepted(configured)
    reads = iter([(), (str(path),)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))
    code, envelope = _answer("apply")
    assert _names(folder) == {LONG}
    assert code == int(ExitCode.PRECONDITION)
    assert _actions(envelope["data"]) == {LONG: "rename"}
    assert "after the plan was approved" in envelope["cause"]["detail"]["incomplete"][0]["why"]
    assert envelope["data"]["totals"]["renamed"] == 0
    # No database was ever built under this library, so the read fails for real.
    monkeypatch.setattr(naming_cli, "_recorded", _REAL_RECORDED)
    code, envelope = _answer("apply")
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert _names(folder) == {LONG}


def _rewrite_payload(cfg, path: Path, **fields: str) -> None:
    """Put values in the stored payload, as an edited import document could."""
    wanted = review.item_id_for(
        str(Queue.PATH_REPAIR), repair.KIND, {"path": str(path.resolve())}
    )
    with review.open_store(cfg) as store:
        payload = {**review.get(store, wanted).payload, **fields}
        with store.immediate() as conn:
            conn.execute(
                "UPDATE review_items SET payload = ? WHERE item_id = ?",
                (json.dumps(payload), wanted),
            )


def _rewrite_proposed(cfg, path: Path, proposed: str) -> None:
    _rewrite_payload(cfg, path, proposed=proposed)


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
    folder, path = _one_accepted(configured)
    _rewrite_proposed(configured, path, proposed)
    code, envelope = _answer("apply")
    assert _names(folder) == {LONG}
    assert not (folder.parent / "escaped.flac").exists()
    assert _actions(envelope["data"]) == {LONG: "unusable"}
    assert code == int(ExitCode.PRECONDITION)
    assert said in envelope["cause"]["detail"]["incomplete"][0]["why"]


def test_an_item_with_no_stored_path_is_held_and_never_guessed_at(configured):
    folder, path = _one_accepted(configured)
    # How an item that arrived by import reads: the identity column is empty.
    with review.open_store(configured) as store, store.immediate() as conn:
        conn.execute("UPDATE review_items SET identity = NULL")
    code, envelope = _answer("apply")
    assert _names(folder) == {LONG}
    assert [item["action"] for item in envelope["data"]["items"]] == ["unusable"]
    assert code == int(ExitCode.PRECONDITION)
    assert "holds no path" in envelope["cause"]["detail"]["incomplete"][0]["why"]
    assert envelope["cause"]["retryable"] is False


def _after_the_gate(monkeypatch, act) -> None:
    """Run ``act`` between the plan's collection read and the apply's."""
    reads = {"count": 0}

    def recorded(cfg):
        reads["count"] += 1
        if reads["count"] == 2:
            act()
        return ()

    monkeypatch.setattr(naming_cli, "_recorded", recorded)


def test_a_name_refused_or_taken_after_the_gate_is_named_and_never_overwritten(configured, monkeypatch):
    folder, path = _one_accepted(configured, b"fLaC mine")

    def refused(target):  # A NAME THE FILESYSTEM REFUSES TO CLAIM is named.
        raise OSError(63, "File name too long")

    claim = naming_cli.naming.claim_target
    monkeypatch.setattr(naming_cli.naming, "claim_target", refused)
    code, envelope = _answer("apply")
    assert _names(folder) == {LONG}
    assert code == int(ExitCode.PRECONDITION)
    assert "File name too long" in envelope["cause"]["detail"]["incomplete"][0]["why"]
    monkeypatch.setattr(naming_cli.naming, "claim_target", claim)
    # A NAME TAKEN AFTER THE GATE is never overwritten.
    _after_the_gate(monkeypatch, lambda: _audio(folder, SHORT, b"fLaC theirs"))
    code, envelope = _answer("apply")
    assert (folder / SHORT).read_bytes() == b"fLaC theirs"
    assert (folder / LONG).read_bytes() == b"fLaC mine"
    assert code == int(ExitCode.PRECONDITION)
    assert _actions(envelope["data"]) == {LONG: "rename"}
    assert "already taken" in envelope["cause"]["detail"]["incomplete"][0]["why"]


def test_a_file_deleted_after_the_gate_is_named_and_not_called_renamed(
    configured, monkeypatch
):
    folder, path = _one_accepted(configured)
    _after_the_gate(monkeypatch, path.unlink)
    code, envelope = _answer("apply")
    assert code == int(ExitCode.PRECONDITION)
    assert "no longer there" in envelope["cause"]["detail"]["incomplete"][0]["why"]
    assert envelope["data"]["totals"]["renamed"] == 0
    assert _names(folder) == set()


def test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder(configured):
    inside = _folder(configured)
    sibling = inside.parent / (inside.name + "s")
    outside = Path(configured.library.root) / "Music" / "other"
    sibling.mkdir()
    outside.mkdir()
    near, twin, far = _audio(inside, LONG), _audio(sibling, LONG), _audio(outside, OTHER_LONG)
    _scan(inside)
    _scan(sibling)
    _scan_accept(configured, outside, near, twin, far)
    # The root typed in another case still names the folder.
    shouted = inside.parent / inside.name.upper()
    code, envelope = _answer("apply", "--root", str(shouted))
    assert code == int(ExitCode.OK), envelope
    assert _names(inside) == {SHORT}
    assert _names(sibling) == {LONG}
    assert _names(outside) == {OTHER_LONG}
    assert envelope["data"]["totals"]["outside_root"] == 2


def test_the_decided_reader_pages_through_a_queue_larger_than_one_page(configured):
    folder = _folder(configured)
    count = review.DEFAULT_PAGE + 3
    for index in range(count):
        _audio(folder, f"04A - 124 - Song{index} - Artist - Song{index}.flac")
    _scan(folder)
    for index in range(count):
        _accept(configured, folder / f"04A - 124 - Song{index} - Artist - Song{index}.flac")
    with review.open_store(configured) as store:
        assert len(repair.decided(store).accepted) == count


