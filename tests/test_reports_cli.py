"""U27's four report verbs, driven through the real dispatcher.

The nine conformance properties are asserted over every entry in
``tests/test_cli_contract.py``, and they drive each of these verbs against an
export that is deliberately absent, which proves the refusal and nothing else.
This module drives the other half: a real export on disk, the answers each verb
gives about it, and the two properties a conformance drive structurally cannot
reach, that the truncation is visible and that a second run of the adjudicating
verb re-offers rather than duplicates.

**No database anywhere.** The reports package is held to an import allowlist that
admits none, so a fixture here needs a configured library and a file, not a
disposable rekordbox database. That is the point rather than a convenience: a
report that needed one would be a report that could commit.

**Zero writes is asserted against the filesystem**, not argued from reading the
code, because the class of defect it guards is a run that wrote something before
it decided not to.
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
    """One export with a filed track, a duplicate pair, and N uncovered tracks.

    ``uncovered`` is a count rather than a fixed shape because the truncation
    property needs more uncovered rows than the limit under test, and a fixture
    that hard coded three would make a limit of two the only limit ever driven.
    """
    tracks = [(1, "08A - 124 - Cold Light", "Recondite", "file://localhost/a.flac")]
    if duplicated:
        tracks.append(
            (2, "11A - 126 - [MP3] Cold  Light", "recondite", "file://localhost/b.flac")
        )
    start = len(tracks) + 1
    tracks += [
        (
            index,
            f"05B - 120 - Loose {index}",
            "Somebody",
            f"file://localhost/loose-{index}.flac",
        )
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


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def configured(library):
    """A set-up machine with no database, which is all a report needs.

    Deliberately NOT the conformance suite's fixture. That one builds a
    disposable rekordbox database because the destructive verbs it drives will
    not admit a machine without one, and copying it here would imply these verbs
    need something they are structurally forbidden from having.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# audit.coverage
# ═══════════════════════════════════════════════════════════════════════════


def test_coverage_reports_the_tracks_the_tree_does_not_file(configured, exported):
    path = exported()
    code, document = envelope_of(["audit", "coverage", str(path)])

    assert code == int(ExitCode.OK)
    summary = document["data"]["summary"]
    assert summary["tree"] == TREE.id
    assert (summary["entries"], summary["covered"], summary["uncovered"]) == (4, 1, 3)
    assert summary["listed"] == 3
    keys = [check["key"] for check in document["data"]["checks"]]
    assert sum(1 for key in keys if key.startswith("uncovered.")) == 3
    assert "coverage.truncated" not in keys


def test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total(
    configured, exported
):
    """A capped list that reads as a complete one is worse than no list.

    The summary's ``uncovered`` comes off the report and ``listed`` off the
    slice, so no limit can make the two agree and hide the cap from a consumer
    that reads only the summary.
    """
    path = exported(uncovered=5)
    code, document = envelope_of(["audit", "coverage", str(path), "--limit", "2"])

    assert code == int(ExitCode.OK)
    summary = document["data"]["summary"]
    assert (summary["uncovered"], summary["listed"]) == (5, 2)
    truncated = [
        check
        for check in document["data"]["checks"]
        if check["key"] == "coverage.truncated"
    ]
    assert len(truncated) == 1
    assert "2 of 5" in truncated[0]["detail"]


def test_a_limit_of_zero_lists_nothing_and_still_counts_everything(configured, exported):
    path = exported()
    _code, document = envelope_of(["audit", "coverage", str(path), "--limit", "0"])
    summary = document["data"]["summary"]
    assert (summary["uncovered"], summary["listed"]) == (3, 0)
    assert any(
        check["key"] == "coverage.truncated" for check in document["data"]["checks"]
    )


def test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end(
    configured, exported
):
    """``uncovered[:-2]`` is a real slice and would list all but the last two.

    A person typing a negative limit means none, and Python's answer to the
    unguarded expression is a silently different list, which is why the handler
    floors it rather than passing it through.
    """
    path = exported()
    _code, document = envelope_of(["audit", "coverage", str(path), "--limit", "-2"])
    assert document["data"]["summary"]["listed"] == 0


def test_coverage_over_an_export_with_no_governed_tree_refuses(configured, library):
    """The refusal reaches the shell with the reserved code rather than a traceback."""
    path = library / "no-tree.xml"
    path.write_bytes(
        _document(
            collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
            root_children=[_folder(INTAKE.display, 0, 1), _close(1)],
            root_count=1,
        )
    )
    code, document = envelope_of(["audit", "coverage", str(path)])
    assert code == int(ExitCode.LIBRARY_PREREQUISITE)
    assert document["cause"]["reason"] == "governed-tree-absent"


def test_a_missing_export_refuses_with_the_readers_own_sentence(configured, library):
    code, document = envelope_of(["audit", "coverage", str(library / "never.xml")])
    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "library-export-unusable"


# ═══════════════════════════════════════════════════════════════════════════
# audit.duplicates
# ═══════════════════════════════════════════════════════════════════════════


def test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key(
    configured, exported
):
    path = exported(duplicated=True)
    code, document = envelope_of(["audit", "duplicates", str(path)])

    assert code == int(ExitCode.OK)
    assert document["data"]["queue"] == str(review.Queue.DUPLICATES)
    assert len(document["data"]["items"]) == 1
    assert document["data"]["unresolved"] == 1
    with review.open_store(configured) as store:
        addressed = review.list_items(store, handler_key="audit.duplicates").items
    assert [item.item_id for item in addressed] == [
        document["data"]["items"][0]["id"]
    ], "the queue cannot show what the verb produced under the name a person typed"


def test_the_two_copies_of_the_duplicate_handler_key_cannot_drift():
    """One verb name lives in two modules, and nothing compared them.

    ``duplicates.HANDLER_KEY`` is the engine's default and
    ``registry.entry("audit.duplicates").handler_key`` is what the shell passes.
    They are the same string today, which is exactly why the author's mutation
    table measured ZERO for dropping the shell's argument: the mutation was
    semantically inert on this tree, so the row said nothing about the wiring.
    What can actually go wrong is the two drifting, and the drift is silent,
    because the queue would still accept items under a key no verb name resolves.
    This is the comparison that was missing.
    """
    assert duplicates.HANDLER_KEY == registry.entry("audit.duplicates").handler_key


def test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default(
    configured, exported, monkeypatch
):
    """The wiring itself, driven, which the inert mutation above could not reach.

    The engine's parameter is a default evaluated when the function is defined,
    so replacing the module constant proves nothing. Wrapping the call and
    reading what the shell actually handed it does.
    """
    seen: list[str | None] = []
    real = duplicates.audit_and_offer

    def recording(view, store, *, template, handler_key=None):
        seen.append(handler_key)
        return real(view, store, template=template, handler_key=handler_key)

    monkeypatch.setattr(reports_cli.duplicates, "audit_and_offer", recording)
    code, _document = envelope_of(["audit", "duplicates", str(exported(duplicated=True))])

    assert code == int(ExitCode.OK)
    assert seen == [registry.entry("audit.duplicates").handler_key]


def test_a_second_run_re_offers_the_same_item_rather_than_a_second_one(
    configured, exported
):
    """Idempotence is the requirement, not an optimization.

    Without it, a person who ran the audit twice would have to answer the same
    pair twice, and the answer they gave the first time would sit beside a
    duplicate of the question.
    """
    path = exported(duplicated=True)
    _first_code, first = envelope_of(["audit", "duplicates", str(path)])
    _second_code, second = envelope_of(["audit", "duplicates", str(path)])

    assert [item["id"] for item in first["data"]["items"]] == [
        item["id"] for item in second["data"]["items"]
    ]
    assert second["data"]["unresolved"] == 1


def test_a_rejected_pair_comes_back_suppressed_rather_than_as_a_question(
    configured, exported
):
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


# ═══════════════════════════════════════════════════════════════════════════
# report.library
# ═══════════════════════════════════════════════════════════════════════════


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
    """Nothing here is a failure, and a report that painted one red would be

    this module deciding what somebody's library should look like.
    """
    _code, document = envelope_of(["report", "library", str(exported())])
    assert {check["status"] for check in document["data"]["checks"]} == {"info"}


# ═══════════════════════════════════════════════════════════════════════════
# report.intake-aging
# ═══════════════════════════════════════════════════════════════════════════


def test_the_aging_report_bands_against_the_day_it_was_asked_for(configured, exported):
    """The flag exists so an answer can be asserted rather than described.

    The fixture's one grouping is dated 2026-06-15, so a run as of 2026-06-20 is
    current and a run as of 2026-12-01 is expired, and the same document produces
    both.
    """
    path = exported()
    _code, fresh = envelope_of(
        ["report", "intake-aging", str(path), "--as-of", "2026-06-20"]
    )
    _code, old = envelope_of(
        ["report", "intake-aging", str(path), "--as-of", "2026-12-01"]
    )

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


def test_an_as_of_that_is_not_a_date_refuses_rather_than_answering_for_today(
    configured, exported
):
    """Defaulting would band every grouping against a value nobody typed."""
    code, document = envelope_of(
        ["report", "intake-aging", str(exported()), "--as-of", "last tuesday"]
    )
    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "report-as-of-invalid"


def test_an_explicitly_empty_as_of_refuses_rather_than_answering_for_today(
    configured, exported
):
    """An empty string is something a person TYPED, so it is not an absent flag.

    FOUND BY THE INDEPENDENT CROSS-MODEL REVIEW, not by this suite, and it is the
    exact failure the refusal beside it was written to prevent: the handler tested
    the value for falsiness, so `--as-of ""` was read as "no flag given" and the
    report aged every grouping against today while exiting OK. Driven before the
    fix: exit 0, outcome ok, as_of today.
    """
    code, document = envelope_of(
        ["report", "intake-aging", str(exported()), "--as-of", ""]
    )
    assert code == int(ExitCode.PRECONDITION)
    assert document["cause"]["reason"] == "report-as-of-invalid"


def test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket(
    configured, library
):
    """Eighteen true rows that bury the one thing that went wrong is not a report.

    The engine reports rather than refuses when the governed tree is absent, which
    is deliberate and argued where it is made. The shell then rendered one gap row
    per declared bucket, so the shipped template produced eighteen of them and the
    actual problem, that the export holds no tree at all, appeared nowhere.
    """
    path = library / "no-tree.xml"
    path.write_bytes(
        _document(
            collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
            root_children=[_folder(INTAKE.display, 0, 1), _close(1)],
            root_count=1,
        )
    )
    _code, document = envelope_of(["report", "library", str(path)])

    gaps = [
        check for check in document["data"]["checks"] if check["key"].startswith("gap.")
    ]
    assert [check["key"] for check in gaps] == ["gap.tree"]
    assert TREE.display in gaps[0]["title"]
    assert document["data"]["summary"]["unused_buckets"] == len(
        default_taxonomy().buckets
    ), "the count still reports every unused bucket; only the rows collapsed"


def test_an_export_with_no_intake_flow_refuses(configured, library):
    path = library / "no-intake.xml"
    path.write_bytes(
        _document(
            collection=_collection([(1, "08A - 124 - A", "B", "file://localhost/a.flac")]),
            root_children=[_folder(TREE.display, 0, 1), _close(1)],
            root_count=1,
        )
    )
    code, document = envelope_of(["report", "intake-aging", str(path)])
    assert code == int(ExitCode.LIBRARY_PREREQUISITE)
    assert document["cause"]["reason"] == "intake-flow-absent"


# ═══════════════════════════════════════════════════════════════════════════
# What none of them does
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "argv",
    [
        ["audit", "coverage"],
        ["report", "library"],
        ["report", "intake-aging"],
    ],
    ids=lambda argv: ".".join(argv),
)
def test_a_read_only_report_changes_nothing_on_the_volume(configured, exported, argv):
    """Asserted against the filesystem, because the defect is a write before a read.

    ``audit.duplicates`` is excluded on purpose and not by oversight: it is the
    one verb here that persists, into the review queue, and R12 is why. Its
    writes are asserted by the queue tests above.
    """
    path = exported()
    before = _fingerprint(configured.library.root)
    code, _document = envelope_of([*argv, str(path)])
    assert code == int(ExitCode.OK)
    assert _fingerprint(configured.library.root) == before


def test_no_report_verb_ever_opens_the_rekordbox_database(configured, exported, monkeypatch):
    """The structural guard is the reports package's import allowlist.

    This is the behavioural half: the database path in the fixture names a file
    that does not exist, so a verb that tried to open one would fail rather than
    quietly succeed against a fixture somebody built for it.
    """
    assert not Path(configured.library.db_path).exists()
    for argv in (
        ["audit", "coverage"],
        ["audit", "duplicates"],
        ["report", "library"],
        ["report", "intake-aging"],
    ):
        code, _document = envelope_of([*argv, str(exported())])
        assert code == int(ExitCode.OK), argv
