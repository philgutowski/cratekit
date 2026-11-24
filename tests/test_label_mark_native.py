"""R-1056: ``label mark --pass`` marks a label batch a native landing filed."""

from __future__ import annotations

import dataclasses
import unicodedata

import pytest

from cratekit.core import config, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import label_filing, native
from cratekit.label import mark_cli as label_mark_cli
from cratekit.label import registry as labels
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import mark_record
from tests.cli_drive import drive
from tests.test_favorites_backfill import _silent as _silent  # noqa: PLC0414
from tests.test_favorites_backfill import silence as silence  # noqa: PLC0414
from tests.test_intake_land_labels_native import _dated, _manifest
from tests.test_intake_land_native import _land, _stage
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import _two_acts as _land_two_acts
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_label_playlists import (
    LABEL,
    MARK,
    _build,
    _exits,
    _faked,
    _landed,
    _reasons,
    _refused,
    _took,
    _two_acts,
)
from tests.test_label_playlists import built as built  # noqa: PLC0414
from tests.test_label_playlists import followed as followed  # noqa: PLC0414
from tests.test_label_playlists import kompakt as kompakt  # noqa: PLC0414
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_label_workers import one_parser as one_parser  # noqa: PLC0414 - fixture
from tests.test_sync_mark import _cut_over_intake

PASS = "LABEL_RUN_synced"
BY_PASS = ["label", "mark", LABEL, "--pass", PASS]


def _filed(year: int, *, label: str = LABEL, tracks: int = 1) -> dict:
    return {"id": f"db-{year}", "name": f"{label} {year}", "label": label, "year": year, "tracks": tracks}


def _record_landing(
    cfg: config.Config, *filed: dict, name: str = PASS,
    state: session.SessionState = session.SessionState.CLOSED,
    source: session.SourceState = session.SourceState.COMMITTED, stamp: str = "120000", labels=None,
) -> str:
    """The session record a native landing given ``--pass name`` commits."""
    started = f"2026-10-07T{stamp[:2]}:{stamp[2:4]}:{stamp[4:]}+00:00"
    detail: dict = {native.PASS_KEY: name}
    if labels is not None:
        detail[label_filing.RECORD_KEY] = labels
    elif filed:
        detail[label_filing.RECORD_KEY] = list(filed)
    record = session.SessionRecord(
        session_id=f"20261007T{stamp}-landing", workflow=native.WORKFLOW, started=started,
        state=state, sources={"intake": str(source)}, ended=started, detail=detail,
    )
    session.write_record(record, cfg)
    return record.session_id


def _mark(option: str = "apply", name: str = PASS) -> tuple[int, dict]:
    return _two_acts(["label", "mark", LABEL, "--pass", name], MARK, option)


@pytest.fixture
def native_followed(followed):
    """Kompakt followed with its three years built, on a native intake tree."""
    cfg, fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    _cut_over_intake(cfg)
    return cfg, fake, account


@pytest.fixture
def native_built(built):
    """``native_built``, its years built by the engine and the label by the store."""
    _cut_over_intake(built[0])
    return built


def test_a_native_pass_marks_exactly_the_years_its_landing_filed(native_built):
    cfg, _fake, account = native_built
    _record_landing(cfg, _filed(2021, tracks=2), _filed(2023))
    refused = _exits(ExitCode.DECISION_REQUIRED, drive(BY_PASS))
    shown = refused["cause"]["detail"]["shown"]
    assert shown["pass"].startswith(f"{PASS}, landed on the database native ")
    assert shown["undone by"] == f"crate sync unmark --pass {PASS}"
    done = _exits(ExitCode.OK, _mark())
    assert _took(account) == ["pl-1", "pl-3"]
    assert _reasons(done)["pl-2"] == label_mark_cli.NOT_IN_BATCH
    held = mark_record.MarkRecord(cfg).taken()
    assert sorted((e.playlist_id, e.name, e.by) for e in held.values()) == [
        ("pl-1", "Kompakt 2021", PASS), ("pl-3", "Kompakt 2023", PASS),
    ]
    assert done["warnings"] == []


def test_every_committed_landing_of_the_pass_counts_and_no_other_does(native_built):
    cfg, _fake, account = native_built
    _record_landing(cfg, _filed(2021), stamp="120000")
    _record_landing(cfg, _filed(2022), stamp="130000")
    # Abandoned, refused, and another pass's: none of these proves a filing.
    _record_landing(cfg, _filed(2023), stamp="140000", state=session.SessionState.ABANDONED)
    _record_landing(cfg, _filed(2023), stamp="150000", source=session.SourceState.REFUSED)
    _record_landing(cfg, _filed(2023), stamp="160000", name="ANOTHER_synced")
    _exits(ExitCode.OK, _mark())
    assert _took(account) == ["pl-1", "pl-2"]


def test_a_year_filed_under_another_label_or_holding_no_track_is_not_marked(native_built):
    cfg, _fake, account = native_built
    _record_landing(cfg, _filed(2021, label="Another Label"), _filed(2022, tracks=0), _filed(2023))
    _exits(ExitCode.OK, _mark())
    assert _took(account) == ["pl-3"]


@pytest.mark.parametrize(
    "filed", [(), (_filed(2021, label="Another Label"),), (_filed(2019),)],
    ids=["no-label-filed", "another-label", "a-year-never-built"],
)
def test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so(
    native_built, filed
):
    cfg, _fake, account = native_built
    _record_landing(cfg, *filed)
    calls = account._writes
    done = _exits(ExitCode.OK, _mark())
    assert done["outcome"] == "no_op" and account.renamed == []
    assert account._writes == calls
    (warned,) = done["warnings"]
    said = f"{LABEL}: {label_mark_cli.NOTHING_FILED_SAID}"
    assert (warned["code"], warned["message"]) == ("label-mark-nothing-filed", said)
    assert {item["reason"] for item in done["data"]["items"]} == {label_mark_cli.NOT_IN_BATCH}


def test_a_bridge_batch_of_another_label_says_it_filed_nothing_too(built):
    cfg, _fake, account = built
    xml = _landed(cfg, label="Another Label")
    done = _exits(ExitCode.OK, _two_acts(["label", "mark", LABEL, "--xml", str(xml)], MARK))
    assert account.renamed == []
    assert [w["code"] for w in done["warnings"]] == ["label-mark-nothing-filed"]


@pytest.mark.parametrize(
    "landing",
    [None, {"state": session.SessionState.ABANDONED}, {"source": session.SourceState.REFUSED},
     {"name": "ANOTHER_synced"}],
    ids=["no-landing", "abandoned", "never-committed", "another-pass"],
)
def test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name(native_built, landing):
    cfg, _fake, account = native_built
    if landing is not None:
        _record_landing(cfg, _filed(2021), **landing)
    calls = account._writes
    refused = _refused(BY_PASS, "sync-marks-blocked")
    assert f"no landing of {PASS!r}" in refused["cause"]["message"]
    assert account._writes == calls and account.renamed == []
    # The label batch's own remedy, not the sync pass's.
    (step,) = refused["cause"]["remediation"]["steps"]
    assert "crate label sync --go" in step and "intake missing" not in step
    assert step.endswith("then run crate label mark --pass with that same name")


def test_a_label_named_by_its_registry_identifier_is_compared_under_its_name(native_built):
    """The identifier is resolved to the name the record holds."""
    cfg, _fake, account = native_built
    _record_landing(cfg, _filed(2021))
    entry = labels.RegistryStore().load().resolve(LABEL)
    assert entry is not None and entry.label_id != LABEL
    _exits(ExitCode.OK, _two_acts(["label", "mark", entry.label_id, "--pass", PASS], MARK))
    assert _took(account) == ["pl-1"]


def test_pass_on_an_intake_tree_on_the_bridge_is_refused_naming_xml(built):
    cfg, _fake, account = built
    _record_landing(cfg, _filed(2021))
    refused = _exits(ExitCode.PRECONDITION, drive(BY_PASS))
    assert "xml bridge" in refused["cause"]["message"]
    assert any("--xml" in step for step in refused["cause"]["remediation"]["steps"])
    assert account.renamed == []


def test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again(
    native_built, monkeypatch
):
    from cratekit.sync import mark_cli as sync_mark_cli
    unreachable = sync_mark_cli.ingest.IntakeMedium(declared=None, registry=None)
    monkeypatch.setattr(sync_mark_cli.ingest, "intake_medium", lambda cfg: unreachable)
    refused = _exits(ExitCode.PRECONDITION, drive(BY_PASS))
    steps = refused["cause"]["remediation"]["steps"]
    assert "mount the library volume, then run crate label mark again" in steps


@pytest.mark.parametrize(
    "argv", [[], ["--xml", "x_inboxed.xml", "--pass", PASS]], ids=["neither", "both"],
)
def test_the_pass_is_named_by_exactly_one_of_the_file_and_the_name(native_built, argv):
    _cfg, _fake, account = native_built
    code, _ = drive(["label", "mark", LABEL, *argv])
    assert code == int(ExitCode.USAGE)
    assert account.renamed == []


@pytest.mark.parametrize(
    "labels",
    [
        "Kompakt 2021", ["Kompakt 2021"], [{"label": LABEL, "year": "2021", "tracks": 1}],
        [{"label": LABEL, "year": 2021}], [{"label": LABEL, "year": True, "tracks": 1}],
        [{"label": LABEL, "year": 2021, "tracks": True}], [{"year": 2021, "tracks": 1}],
    ],
    ids=[
        "a-string", "a-list-of-strings", "a-text-year", "no-tracks", "a-bool-year", "a-bool-tracks",
        "no-label",
    ],
)
def test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused(
    native_built, labels
):
    cfg, _fake, account = native_built
    session_id = _record_landing(cfg, labels=labels)
    refused = _exits(ExitCode.PRECONDITION, drive(BY_PASS))
    assert session_id in refused["cause"]["message"]
    assert "cannot read" in refused["cause"]["message"]
    assert account.renamed == []


def test_a_landing_of_the_pass_after_the_answer_makes_it_stale(native_built):
    cfg, _fake, account = native_built
    _record_landing(cfg, _filed(2021))
    refused = _exits(ExitCode.DECISION_REQUIRED, drive(BY_PASS))
    run_id = refused["run_id"]
    _exits(ExitCode.OK, drive(["run", "decide", run_id, MARK, "apply", "--actor", "a-person"]))
    # The same year again, so the marks alone would not move the digest.
    _record_landing(cfg, _filed(2021), stamp="130000")
    _exits(ExitCode.DECISION_STALE, drive(["--run", run_id, *BY_PASS]))
    assert account.renamed == []


def test_a_landing_between_the_plan_and_the_first_rename_renames_nothing(native_built, monkeypatch):
    """The run's own reread of the proof, which no gate stands between."""
    cfg, _fake, account = native_built
    _record_landing(cfg, _filed(2021))
    real = label_mark_cli.native_proof
    seen: list[str] = []
    def proving(cfg, name, *, verb, named):
        seen.append(verb)
        if len(seen) == 3:
            # The applying run's second read: a landing since its plan.
            _record_landing(cfg, _filed(2021), stamp="130000")
        return real(cfg, name, verb=verb, named=named)
    monkeypatch.setattr(label_mark_cli, "native_proof", proving)
    refused = _exits(ExitCode.PRECONDITION, _mark())
    assert "changed since the plan" in refused["cause"]["message"]
    assert seen == ["crate label mark"] * 3
    assert account.renamed == []
    assert not mark_record.MarkRecord(cfg).taken()


def test_sync_unmark_takes_a_native_label_mark_off_again(native_built):
    cfg, fake, account = native_built
    _record_landing(cfg, _filed(2021), _filed(2022), _filed(2023))
    assert _mark()[0] == int(ExitCode.OK)
    fake.account = [
        AccountPlaylist(playlist_id=pid, name=title, tracks=None)
        for pid, title in account.titles.items()
    ]
    account.renamed.clear()
    _exits(ExitCode.OK, _two_acts(["sync", "unmark", "--pass", PASS], "sync.unmark.confirm"))
    assert account.renamed == [], "a release writes nothing on the account (U242)"
    assert mark_record.MarkRecord(cfg).taken_ids() == frozenset()


def _record(labels) -> session.SessionRecord:
    return session.SessionRecord(
        session_id="20261007T120000-landing", workflow=native.WORKFLOW,
        started="2026-10-07T12:00:00+00:00", state=session.SessionState.CLOSED, sources={},
        detail={} if labels is None else {label_filing.RECORD_KEY: labels},
    )


@pytest.mark.parametrize(
    ("filing", "years"),
    [
        pytest.param(None, set(), id="no-label-filing-filed-no-year"),
        pytest.param([], set(), id="an-empty-label-filing-filed-no-year"),
        pytest.param([_filed(2021, label="kompakt"), _filed(2022, label="Kompakt ")], set(),
                     id="a-label-is-compared-exactly-otherwise"),
        pytest.param([_filed(987), _filed(2021, tracks=3)], {"0987", "2021"},
                     id="a-year-is-four-digits-as-the-ledger-spells-it"),
    ],
)
def test_a_record_filed_the_years_its_label_filing_names(filing, years):
    assert label_filing.years_filed(_record(filing), LABEL) == frozenset(years)


def test_a_label_spelled_decomposed_on_either_side_is_the_same_label():
    composed = unicodedata.normalize("NFC", "Kompäkt")
    decomposed = unicodedata.normalize("NFD", composed)
    assert composed != decomposed
    for written, asked in ((decomposed, composed), (composed, decomposed)):
        assert label_filing.years_filed(_record([_filed(2021, label=written)]), asked) == {"2021"}


@pytest.fixture
def landed_natively(native_library, monkeypatch):
    """The native landing machine; ``follow`` then follows Kompakt and builds its years."""
    cfg, _root = native_library
    def follow():
        config.save(dataclasses.replace(cfg, profile=config.ProfileConfig(name="full")))
        config.reset_cache()
        labels.RegistryStore().add(LABEL)
        _cfg, _fake, account = _faked(monkeypatch, cfg)
        assert _build()[0] == int(ExitCode.OK)
        return account
    return cfg, follow


def test_a_label_batch_landed_natively_with_label_is_marked_by_its_pass(landed_natively, silence):
    cfg, follow = landed_natively
    _dated(cfg, silence, "One.flac", "2021-03-01")
    _dated(cfg, silence, "Two.flac", "2023-05-01")
    code, acted, _ = _land_two_acts(_land("--label", LABEL, "--pass", PASS))
    assert code == int(ExitCode.OK), acted
    account = follow()
    done = _exits(ExitCode.OK, _mark())
    assert _took(account) == ["pl-1", "pl-3"]
    assert _reasons(done)["pl-2"] == label_mark_cli.NOT_IN_BATCH


def test_a_label_batch_landed_natively_with_a_manifest_is_marked_by_its_pass(
    landed_natively, silence, tmp_path
):
    cfg, follow = landed_natively
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    rows = [("1", "Probe", "One", LABEL, 2022), ("2", "Probe", "Two", "Another Label", 2023)]
    manifest = _manifest(tmp_path, rows)
    code, acted, _ = _land_two_acts(_land("--manifest", str(manifest), "--pass", PASS))
    assert code == int(ExitCode.OK), acted
    account = follow()
    _exits(ExitCode.OK, _mark())
    assert _took(account) == ["pl-2"]


def test_the_gate_digest_names_the_landings(native_built):
    """What makes a second landing another plan, read off the payload itself."""
    cfg, _fake, _account = native_built
    _record_landing(cfg, _filed(2021))
    first = _exits(ExitCode.DECISION_REQUIRED, drive(BY_PASS))
    _record_landing(cfg, _filed(2021), stamp="130000")
    second = _exits(ExitCode.DECISION_REQUIRED, drive(BY_PASS))
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]

