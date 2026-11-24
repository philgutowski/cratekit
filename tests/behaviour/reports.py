"""The report verbs' scenarios: the tables each prints and the queue one writes (U311).

Each reads the report suite's export, rendered and as JSON; the duplicate
audit's queue is held after each of three runs, the last after its pair is rejected.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.modules.test_reports import _close, _collection, _document, _folder
from tests.test_reports_cli import INTAKE, TREE
from tests.test_reports_cli import configured as configured  # noqa: PLC0414
from tests.test_reports_cli import exported as exported  # noqa: PLC0414
from tests.test_reports_cli import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def _one_track_export(path, folder: str):
    """An export of one track under one empty top level folder, as the suite writes it."""
    path.write_bytes(
        _document(
            collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
            root_children=[_folder(folder, 0, 1), _close(1)],
            root_count=1,
        )
    )
    return path


def _both(stage, *argv: str):
    """The verb in a person's rendering and then as JSON, returning the JSON run."""
    shown = stage.crate(*argv)
    ran = stage.json(*argv)
    assert shown.code == ran.code, shown.stderr
    return ran


def test_coverage_lists_what_the_tree_does_not_file(stage, configured, exported):
    path = exported(uncovered=5)
    assert _both(stage, "audit", "coverage", path).code == OK
    assert _both(stage, "audit", "coverage", path, "--limit", "2").code == OK
    assert _both(stage, "audit", "coverage", path, "--limit", "0").code == OK


def test_duplicates_offer_a_pair_into_the_review_queue(stage, configured, exported):
    path = exported(duplicated=True)
    first = _both(stage, "audit", "duplicates", path)
    assert first.code == OK, first.stdout
    item_id = first.envelope["data"]["items"][0]["id"]
    assert _both(stage, "audit", "duplicates", path).code == OK
    rejected = stage.json("review", "resolve", item_id, "--verdict", "rejected")
    assert rejected.code == OK, rejected.stdout
    assert _both(stage, "audit", "duplicates", path).code == OK
    assert _both(stage, "audit", "duplicates", exported()).code == OK


def test_the_library_report_names_its_genres_and_gaps(stage, configured, exported, library):
    assert _both(stage, "report", "library", exported()).code == OK
    no_tree = _one_track_export(library / "no-tree.xml", INTAKE.display)
    assert _both(stage, "report", "library", no_tree).code == OK


def test_the_aging_report_bands_each_grouping(stage, configured, exported, library):
    path = exported()
    assert _both(stage, "report", "intake-aging", path).code == OK
    assert _both(stage, "report", "intake-aging", path, "--as-of", "2026-06-20").code == OK
    assert _both(stage, "report", "intake-aging", path, "--as-of", "2026-12-01").code == OK
    refused = _both(stage, "report", "intake-aging", path, "--as-of", "last tuesday")
    assert refused.code == int(ExitCode.PRECONDITION), refused.stdout
    no_intake = _one_track_export(library / "no-intake.xml", TREE.display)
    refused = _both(stage, "report", "intake-aging", no_intake)
    assert refused.code == int(ExitCode.LIBRARY_PREREQUISITE), refused.stdout


def test_a_report_refuses_an_export_it_cannot_read(stage, configured, library):
    missing = library / "never.xml"
    for argv in (
        ("audit", "coverage"),
        ("audit", "duplicates"),
        ("report", "library"),
        ("report", "intake-aging"),
    ):
        assert _both(stage, *argv, missing).code != OK
    no_tree = _one_track_export(library / "no-tree.xml", INTAKE.display)
    assert _both(stage, "audit", "coverage", no_tree).code != OK
