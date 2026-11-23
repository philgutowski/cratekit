"""The four report verbs, driven through the real dispatcher on a real export.

Truncation is visible, a rerun re-offers rather than duplicates, and no fixture
builds a database, since the reports package may import none.
"""

from __future__ import annotations

import io
import json
import os
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output, registry
from cratekit.cli import reports as reports_cli
from cratekit.core import config, review
from cratekit.core.exit_codes import ExitCode
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.core.taxonomy import default_taxonomy
from cratekit.modules.reports import duplicates
from tests.modules.test_reports import _close, _collection, _document, _folder, _playlist

TREE = default_taxonomy().tree
INTAKE = default_taxonomy().intake
DEEP = default_taxonomy().bucket("deep_house")
TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))


def _export_bytes(*, duplicated: bool = False, uncovered: int = 3) -> bytes:
    """One export with a filed track, a duplicate pair, and N uncovered tracks."""
    tracks = [(1, "08A - 124 - Cold Light", "Recondite", "file://localhost/a.flac")]
    if duplicated:
        tracks.append((2, "11A - 126 - [MP3] Cold  Light", "recondite", "file://localhost/b.flac"))
    start = len(tracks) + 1
    tracks += [
        (index, f"05B - 120 - Loose {index}", "Somebody", f"file://localhost/loose-{index}.flac")
        for index in range(start, start + uncovered)
    ]
    loose_ids = [index for index in range(start, start + uncovered)]
    return _document(
        collection=_collection(tracks),
        root_children=[
            _folder(TREE.display, 1, 1),
            _folder(DEEP.display, 1, 2),
            *_playlist("High", [1], 3),
            _close(2),
            _close(1),
            _folder(INTAKE.display, 1, 1),
            *_playlist("2026-06-15 bandcamp", loose_ids, 2),
            _close(1),
        ],
        root_count=2,
    )


def _one_folder_export(path: Path, display: str) -> Path:
    """An export of one track whose tree holds a single empty folder."""
    path.write_bytes(
        _document(
            collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
            root_children=[_folder(display, 0, 1), _close(1)],
            root_count=1,
        )
    )
    return path


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library):
    """A set up machine with no database, which is all a report needs."""
    cfg = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(cfg)
    config.reset_cache()
    return cfg


@pytest.fixture
def exported(library):
    def write(**kwargs) -> Path:
        path = library / "collection.xml"
        path.write_bytes(_export_bytes(**kwargs))
        return path

    return write


def drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def envelope_of(argv: list[str]) -> tuple[int, dict]:
    code, out, err = drive(["--output", "json", *argv])
    assert out.strip(), err
    document = json.loads(out)
    assert output.envelope_problems(document) == [], document
    return code, document


def _fingerprint(root: Path) -> dict[str, tuple[int, int]]:
    found: dict[str, tuple[int, int]] = {}
    for current, _directories, files in os.walk(root):
        for name in files:
            path = Path(current) / name
            stat = path.stat()
            found[str(path)] = (stat.st_size, stat.st_mtime_ns)
    return found


# audit.coverage


def test_coverage_reports_the_tracks_the_tree_does_not_file(configured, exported):
    code, document = envelope_of(["audit", "coverage", str(exported())])

    assert code == int(ExitCode.OK)
    summary = document["data"]["summary"]
    assert summary["tree"] == TREE.id
    assert (summary["entries"], summary["covered"], summary["uncovered"]) == (4, 1, 3)
    assert summary["listed"] == 3
    keys = [check["key"] for check in document["data"]["checks"]]
    assert sum(1 for key in keys if key.startswith("uncovered.")) == 3
    assert "coverage.truncated" not in keys


def test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total(configured, exported):
    """``uncovered`` comes off the report and ``listed`` off the slice, so a cap shows."""
    path = exported(uncovered=5)
    code, document = envelope_of(["audit", "coverage", str(path), "--limit", "2"])

    assert code == int(ExitCode.OK)
    summary = document["data"]["summary"]
    assert (summary["uncovered"], summary["listed"]) == (5, 2)
    checks = document["data"]["checks"]
    truncated = [check for check in checks if check["key"] == "coverage.truncated"]
    assert len(truncated) == 1
    assert "2 of 5" in truncated[0]["detail"]


def test_a_limit_of_zero_lists_nothing_and_still_counts_everything(configured, exported):
    _code, document = envelope_of(["audit", "coverage", str(exported()), "--limit", "0"])
    summary = document["data"]["summary"]
    assert (summary["uncovered"], summary["listed"]) == (3, 0)
    assert any(check["key"] == "coverage.truncated" for check in document["data"]["checks"])


def test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end(configured, exported):
    """``uncovered[:-2]`` would silently list all but the last two."""
    _code, document = envelope_of(["audit", "coverage", str(exported()), "--limit", "-2"])
    assert document["data"]["summary"]["listed"] == 0


def test_coverage_over_an_export_with_no_governed_tree_refuses(configured, library):
    """The refusal reaches the shell with the reserved code, not a traceback."""
    path = _one_folder_export(library / "no-tree.xml", INTAKE.display)
    code, document = envelope_of(["audit", "coverage", str(path)])
    assert code == int(ExitCode.LIBRARY_PREREQUISITE)
    assert document["cause"]["reason"] == "governed-tree-absent"


def test_a_missing_export_refuses_with_the_readers_own_sentence(configured, library):
    code, document = envelope_of(["audit", "coverage", str(library / "never.xml")])
    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "library-export-unusable"


# audit.duplicates


def test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key(configured, exported):
    code, document = envelope_of(["audit", "duplicates", str(exported(duplicated=True))])

    assert code == int(ExitCode.OK)
    assert document["data"]["queue"] == str(review.Queue.DUPLICATES)
    assert len(document["data"]["items"]) == 1
    assert document["data"]["unresolved"] == 1
    with review.open_store(configured) as store:
        addressed = review.list_items(store, handler_key="audit.duplicates").items
    assert [item.item_id for item in addressed] == [document["data"]["items"][0]["id"]], (
        "the queue cannot show what the verb produced under the name a person typed"
    )


def test_the_two_copies_of_the_duplicate_handler_key_cannot_drift():
    """The engine's default and the registry's key name one verb in two modules."""
    assert duplicates.HANDLER_KEY == registry.entry("audit.duplicates").handler_key


def test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default(
    configured, exported, monkeypatch
):
    """The wiring, read off what the shell actually hands the engine."""
    seen: list[str | None] = []
    real = duplicates.audit_and_offer

    def recording(view, store, *, template, handler_key=None):
        seen.append(handler_key)
        return real(view, store, template=template, handler_key=handler_key)

    monkeypatch.setattr(reports_cli.duplicates, "audit_and_offer", recording)
    code, _document = envelope_of(["audit", "duplicates", str(exported(duplicated=True))])

    assert code == int(ExitCode.OK)
    assert seen == [registry.entry("audit.duplicates").handler_key]


def test_a_second_run_re_offers_the_same_item_rather_than_a_second_one(configured, exported):
    """Idempotence: a pair answered once is never asked twice."""
    path = exported(duplicated=True)
    _first_code, first = envelope_of(["audit", "duplicates", str(path)])
    _second_code, second = envelope_of(["audit", "duplicates", str(path)])

    assert [item["id"] for item in first["data"]["items"]] == [
        item["id"] for item in second["data"]["items"]
    ]
    assert second["data"]["unresolved"] == 1


def test_a_rejected_pair_comes_back_suppressed_rather_than_as_a_question(configured, exported):
    """The persistent ignore R12 asks for, arrived at with no file of our own."""
    path = exported(duplicated=True)
    _code, first = envelope_of(["audit", "duplicates", str(path)])
    item_id = first["data"]["items"][0]["id"]
    resolved, _out, err = drive(
        ["--output", "json", "review", "resolve", item_id, "--verdict", "rejected"]
    )
    assert resolved == int(ExitCode.OK), err

    _again, second = envelope_of(["audit", "duplicates", str(path)])
    assert second["data"]["unresolved"] == 0
    assert second["data"]["items"][0]["verdict"] == str(review.Verdict.REJECTED)


def test_an_export_with_no_repeated_recording_reports_no_op(configured, exported):
    _code, document = envelope_of(["audit", "duplicates", str(exported())])
    assert document["outcome"] == "no_op"
    assert document["data"]["items"] == []


# report.library


def test_the_library_report_names_the_genres_and_the_gaps(configured, exported):
    _code, document = envelope_of(["report", "library", str(exported())])
    summary = document["data"]["summary"]
    assert summary["tree"] == TREE.id
    assert summary["entries"] == 4
    assert summary["genres"] == 1
    assert summary["in_no_playlist"] == 0
    assert summary["deeper_than_declared"] is False

    keys = [check["key"] for check in document["data"]["checks"]]
    assert f"genre.{DEEP.id}" in keys
    assert "tempo.spread" in keys
    assert "tree.shape" in keys


def test_every_row_of_the_library_report_is_informational(configured, exported):
    """Nothing here is a failure; the library is the person's to judge."""
    _code, document = envelope_of(["report", "library", str(exported())])
    assert {check["status"] for check in document["data"]["checks"]} == {"info"}


def test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket(configured, library):
    """One ``gap.tree`` row, not one gap row per declared bucket burying it."""
    path = _one_folder_export(library / "no-tree.xml", INTAKE.display)
    _code, document = envelope_of(["report", "library", str(path)])

    checks = document["data"]["checks"]
    gaps = [check for check in checks if check["key"].startswith("gap.")]
    assert [check["key"] for check in gaps] == ["gap.tree"]
    assert TREE.display in gaps[0]["title"]
    assert document["data"]["summary"]["unused_buckets"] == len(default_taxonomy().buckets), (
        "the count still reports every unused bucket; only the rows collapsed"
    )


# report.intake-aging


def test_the_aging_report_bands_against_the_day_it_was_asked_for(configured, exported):
    """The one grouping is dated 2026-06-15: current on 06-20, expired on 12-01."""
    path = exported()
    _code, fresh = envelope_of(["report", "intake-aging", str(path), "--as-of", "2026-06-20"])
    _code, old = envelope_of(["report", "intake-aging", str(path), "--as-of", "2026-12-01"])

    assert fresh["data"]["summary"]["current"] == 1
    assert fresh["data"]["summary"]["expired"] == 0
    assert old["data"]["summary"]["expired"] == 1
    assert old["data"]["summary"]["current"] == 0
    assert fresh["data"]["summary"]["as_of"] == "2026-06-20"


def test_the_thresholds_come_from_configuration_and_are_reported(configured, exported):
    _code, document = envelope_of(["report", "intake-aging", str(exported())])
    summary = document["data"]["summary"]
    assert summary["stale_days"] == configured.reports.intake_stale_days
    assert summary["expired_days"] == configured.reports.intake_expired_days


@pytest.mark.parametrize("as_of", ["last tuesday", ""], ids=["not a date", "empty"])
def test_an_as_of_that_is_not_a_date_refuses_rather_than_answering_for_today(
    configured, exported, as_of
):
    """An empty string was typed, so it is not an absent flag to default."""
    code, document = envelope_of(["report", "intake-aging", str(exported()), "--as-of", as_of])
    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "report-as-of-invalid"


def test_an_export_with_no_intake_flow_refuses(configured, library):
    path = _one_folder_export(library / "no-intake.xml", TREE.display)
    code, document = envelope_of(["report", "intake-aging", str(path)])
    assert code == int(ExitCode.LIBRARY_PREREQUISITE)
    assert document["cause"]["reason"] == "intake-flow-absent"


# What none of them does


@pytest.mark.parametrize(
    "argv",
    [["audit", "coverage"], ["report", "library"], ["report", "intake-aging"]],
    ids=lambda argv: ".".join(argv),
)
def test_a_read_only_report_changes_nothing_on_the_volume(configured, exported, argv):
    """Against the filesystem; ``audit.duplicates`` persists into the queue (R12)."""
    path = exported()
    before = _fingerprint(configured.library.root)
    code, _document = envelope_of([*argv, str(path)])
    assert code == int(ExitCode.OK)
    assert _fingerprint(configured.library.root) == before


def test_no_report_verb_ever_opens_the_rekordbox_database(configured, exported, monkeypatch):
    """The configured database path does not exist, so a verb opening it fails."""
    assert not Path(configured.library.db_path).exists()
    for argv in (
        ["audit", "coverage"],
        ["audit", "duplicates"],
        ["report", "library"],
        ["report", "intake-aging"],
    ):
        code, _document = envelope_of([*argv, str(exported())])
        assert code == int(ExitCode.OK), argv
