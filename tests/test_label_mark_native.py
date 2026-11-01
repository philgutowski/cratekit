"""R-1056: ``label mark --pass`` marks a label batch a native landing filed.

A native landing writes no intake file, so ``label mark --xml`` had nothing to
read once U156 let a native landing file a label batch under Record Labels.
Named by its pass, the mark is proved the way ``sync mark --pass`` is proved,
and the label and years filed are read off the ``labels`` entries the
landing's session record carries. Every other rule is the bridge's, which
``tests/test_label_playlists.py`` drives unchanged.

Two halves. The first writes the landing's session record by hand, as
``tests/test_sync_mark.py`` does for ``sync mark --pass``, so each rule is
driven alone. The second lands a real batch natively, with ``--label`` and
with ``--manifest``, on the disposable database the native landing suite
builds, and marks it.

D1 applies. Nothing here names a real volume, a real person or a real track.
"""

from __future__ import annotations

import dataclasses
import unicodedata

import pytest

from cratekit.core import config, session
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import label_filing, native
from cratekit.label import catalogue
from cratekit.label import mark_cli as label_mark_cli
from cratekit.label.catalogue import AccountPlaylist
from cratekit.sync import mark_record
from tests import outbound_fakes
from tests.cli_drive import drive
from tests.label_fakes import catalogue_factory
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
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_label_playlists import LABEL, MARK, _build, _catalogue, _landed, _two_acts
from tests.test_label_playlists import followed as followed  # noqa: PLC0414
from tests.test_label_workers import installed as installed  # noqa: PLC0414
from tests.test_label_workers import register
from tests.test_outbound_workers import bind as bind_account
from tests.test_sync_mark import _cut_over_intake

PASS = "LABEL_RUN_synced"

#: Every year the followed label's build makes, by the fake account's id.
BUILT = {"pl-1": "Kompakt 2021", "pl-2": "Kompakt 2022", "pl-3": "Kompakt 2023"}


def _filed(year: int, *, label: str = LABEL, tracks: int = 1) -> dict:
    """One entry as ``label_filing.record_commit`` writes it."""
    return {"id": f"db-{year}", "name": f"{label} {year}", "label": label, "year": year, "tracks": tracks}


def _record_landing(
    cfg: config.Config,
    *filed: dict,
    name: str = PASS,
    state: session.SessionState = session.SessionState.CLOSED,
    source: session.SourceState = session.SourceState.COMMITTED,
    stamp: str = "120000",
    labels=None,
) -> str:
    """The session record a native landing given ``--pass name`` commits,
    with the year playlists it filed under ``labels``."""
    started = f"2026-10-07T{stamp[:2]}:{stamp[2:4]}:{stamp[4:]}+00:00"
    detail: dict = {native.PASS_KEY: name}
    if labels is not None:
        detail[label_filing.RECORD_KEY] = labels
    elif filed:
        detail[label_filing.RECORD_KEY] = list(filed)
    record = session.SessionRecord(
        session_id=f"20261007T{stamp}-landing",
        workflow=native.WORKFLOW,
        started=started,
        state=state,
        sources={"intake": str(source)},
        ended=started,
        detail=detail,
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


# ═══════════════════════════════════════════════════════════════════════════
# 1. The years are the landings' own
# ═══════════════════════════════════════════════════════════════════════════


def test_a_native_pass_marks_exactly_the_years_its_landing_filed(native_followed):
    cfg, _fake, account = native_followed
    _record_landing(cfg, _filed(2021, tracks=2), _filed(2023))

    code, refused = drive(["label", "mark", LABEL, "--pass", PASS])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    assert shown["pass"].startswith(f"{PASS}, landed on the database native ")
    assert shown["undone by"] == f"crate sync unmark --pass {PASS}"
    code, done = _mark()

    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-1", "DOWNLOADED Kompakt 2021"),
        ("pl-3", "DOWNLOADED Kompakt 2023"),
    ]
    reasons = {item["id"]: item.get("reason") for item in done["data"]["items"]}
    assert reasons["pl-2"] == label_mark_cli.NOT_IN_BATCH
    held = mark_record.MarkRecord(cfg).of_pass(PASS)
    assert sorted((e.playlist_id, e.name, e.to) for e in held) == [
        ("pl-1", "Kompakt 2021", "DOWNLOADED Kompakt 2021"),
        ("pl-3", "Kompakt 2023", "DOWNLOADED Kompakt 2023"),
    ]
    assert done["warnings"] == []


def test_every_committed_landing_of_the_pass_counts_and_no_other_does(native_followed):
    cfg, _fake, account = native_followed
    _record_landing(cfg, _filed(2021), stamp="120000")
    _record_landing(cfg, _filed(2022), stamp="130000")
    # Abandoned, refused, and another pass's: none of these proves a filing.
    _record_landing(cfg, _filed(2023), stamp="140000", state=session.SessionState.ABANDONED)
    _record_landing(cfg, _filed(2023), stamp="150000", source=session.SourceState.REFUSED)
    _record_landing(cfg, _filed(2023), stamp="160000", name="ANOTHER_synced")

    code, done = _mark()

    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-1", "DOWNLOADED Kompakt 2021"),
        ("pl-2", "DOWNLOADED Kompakt 2022"),
    ]


def test_a_year_filed_under_another_label_or_holding_no_track_is_not_marked(native_followed):
    cfg, _fake, account = native_followed
    _record_landing(
        cfg, _filed(2021, label="Another Label"), _filed(2022, tracks=0), _filed(2023)
    )

    code, done = _mark()

    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-3", "DOWNLOADED Kompakt 2023")]


# ═══════════════════════════════════════════════════════════════════════════
# 2. Nothing filed, and no proof
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "filed",
    [(), (_filed(2021, label="Another Label"),), (_filed(2019),)],
    ids=["no-label-filed", "another-label", "a-year-never-built"],
)
def test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so(
    native_followed, filed
):
    cfg, _fake, account = native_followed
    _record_landing(cfg, *filed)
    calls = account._writes

    code, done = _mark()

    assert code == int(ExitCode.OK), done
    assert done["outcome"] == "no_op" and account.renamed == []
    assert account._writes == calls
    (warned,) = done["warnings"]
    assert warned["code"] == "label-mark-nothing-filed"
    assert warned["message"] == f"{LABEL}: {label_mark_cli.NOTHING_FILED_SAID}"
    assert {item["reason"] for item in done["data"]["items"]} == {label_mark_cli.NOT_IN_BATCH}


def test_a_bridge_batch_of_another_label_says_it_filed_nothing_too(followed):
    cfg, _fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    xml = _landed(cfg, label="Another Label")

    code, done = _two_acts(["label", "mark", LABEL, "--xml", str(xml)], MARK)

    assert code == int(ExitCode.OK), done
    assert account.renamed == []
    assert [w["code"] for w in done["warnings"]] == ["label-mark-nothing-filed"]


@pytest.mark.parametrize(
    "landing",
    [
        None,
        {"state": session.SessionState.ABANDONED},
        {"source": session.SourceState.REFUSED},
        {"name": "ANOTHER_synced"},
    ],
    ids=["no-landing", "abandoned", "never-committed", "another-pass"],
)
def test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name(
    native_followed, landing
):
    cfg, _fake, account = native_followed
    if landing is not None:
        _record_landing(cfg, _filed(2021), **landing)
    calls = account._writes

    code, refused = drive(["label", "mark", LABEL, "--pass", PASS])

    assert code == int(ExitCode.PRECONDITION), refused
    assert refused["cause"]["reason"] == "sync-marks-blocked"
    assert f"no landing of {PASS!r}" in refused["cause"]["message"]
    assert account._writes == calls and account.renamed == []


def test_pass_on_an_intake_tree_on_the_bridge_is_refused_naming_xml(followed):
    cfg, _fake, account = followed
    assert _build()[0] == int(ExitCode.OK)
    _record_landing(cfg, _filed(2021))

    code, refused = drive(["label", "mark", LABEL, "--pass", PASS])

    assert code == int(ExitCode.PRECONDITION), refused
    assert "xml bridge" in refused["cause"]["message"]
    assert any("--xml" in step for step in refused["cause"]["remediation"]["steps"])
    assert account.renamed == []


def test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again(
    native_followed, monkeypatch
):
    from cratekit.sync import mark_cli as sync_mark_cli

    monkeypatch.setattr(
        sync_mark_cli.ingest,
        "intake_medium",
        lambda cfg: sync_mark_cli.ingest.IntakeMedium(declared=None, registry=None),
    )
    code, refused = drive(["label", "mark", LABEL, "--pass", PASS])
    assert code == int(ExitCode.PRECONDITION), refused
    steps = refused["cause"]["remediation"]["steps"]
    assert "mount the library volume, then run crate label mark again" in steps


@pytest.mark.parametrize(
    "argv",
    [[], ["--xml", "x_inboxed.xml", "--pass", PASS]],
    ids=["neither", "both"],
)
def test_the_pass_is_named_by_exactly_one_of_the_file_and_the_name(native_followed, argv):
    _cfg, _fake, account = native_followed
    code, _ = drive(["label", "mark", LABEL, *argv])
    assert code == int(ExitCode.USAGE)
    assert account.renamed == []


@pytest.mark.parametrize(
    "labels",
    [
        "Kompakt 2021",
        ["Kompakt 2021"],
        [{"label": LABEL, "year": "2021", "tracks": 1}],
        [{"label": LABEL, "year": 2021}],
        [{"label": LABEL, "year": True, "tracks": 1}],
        [{"year": 2021, "tracks": 1}],
    ],
    ids=["a-string", "a-list-of-strings", "a-text-year", "no-tracks", "a-bool-year", "no-label"],
)
def test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused(
    native_followed, labels
):
    cfg, _fake, account = native_followed
    session_id = _record_landing(cfg, labels=labels)

    code, refused = drive(["label", "mark", LABEL, "--pass", PASS])

    assert code == int(ExitCode.PRECONDITION), refused
    assert session_id in refused["cause"]["message"]
    assert "cannot read" in refused["cause"]["message"]
    assert account.renamed == []


# ═══════════════════════════════════════════════════════════════════════════
# 3. The answer covers the landings it was shown
# ═══════════════════════════════════════════════════════════════════════════


def test_a_landing_of_the_pass_after_the_answer_makes_it_stale(native_followed):
    cfg, _fake, account = native_followed
    _record_landing(cfg, _filed(2021))
    code, refused = drive(["label", "mark", LABEL, "--pass", PASS])
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    code, _ = drive(["run", "decide", run_id, MARK, "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK)
    # The same year again, so the marks alone would not move the digest.
    _record_landing(cfg, _filed(2021), stamp="130000")

    code, stale = drive(["--run", run_id, "label", "mark", LABEL, "--pass", PASS])

    assert code == int(ExitCode.DECISION_STALE), stale
    assert account.renamed == []


def test_a_landing_between_the_plan_and_the_first_rename_renames_nothing(
    native_followed, monkeypatch
):
    """The run's own reread of the proof, which no gate stands between."""
    cfg, _fake, account = native_followed
    _record_landing(cfg, _filed(2021))
    real = label_mark_cli.native_proof
    seen: list[str] = []

    def proving(cfg, name, *, verb):
        seen.append(verb)
        if len(seen) == 3:
            # The applying run's second read: a landing since its plan.
            _record_landing(cfg, _filed(2021), stamp="130000")
        return real(cfg, name, verb=verb)

    monkeypatch.setattr(label_mark_cli, "native_proof", proving)

    code, refused = _mark()

    assert code == int(ExitCode.PRECONDITION), refused
    assert "changed since the plan" in refused["cause"]["message"]
    assert seen == ["crate label mark"] * 3
    assert account.renamed == []
    assert not mark_record.MarkRecord(cfg).of_pass(PASS)


def test_sync_unmark_takes_a_native_label_mark_off_again(native_followed):
    cfg, fake, account = native_followed
    _record_landing(cfg, _filed(2021), _filed(2022), _filed(2023))
    assert _mark()[0] == int(ExitCode.OK)
    fake.account = [
        AccountPlaylist(playlist_id=pid, name=title, tracks=None)
        for pid, title in account.titles.items()
    ]
    account.renamed.clear()

    code, done = _two_acts(["sync", "unmark", "--pass", PASS], "sync.unmark.confirm")

    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == sorted(BUILT.items())


# ═══════════════════════════════════════════════════════════════════════════
# 4. The record reader
# ═══════════════════════════════════════════════════════════════════════════


#: The session the reader's own records are read as.
ONE_LANDING = "20261007T120000-landing"


def _record(labels) -> session.SessionRecord:
    return session.SessionRecord(
        session_id=ONE_LANDING,
        workflow=native.WORKFLOW,
        started="2026-10-07T12:00:00+00:00",
        state=session.SessionState.CLOSED,
        sources={},
        detail={} if labels is None else {label_filing.RECORD_KEY: labels},
    )


def test_a_record_with_no_label_filing_filed_no_year():
    assert label_filing.years_filed(_record(None), LABEL) == frozenset()
    assert label_filing.years_filed(_record([]), LABEL) == frozenset()


def test_a_label_spelled_decomposed_on_either_side_is_the_same_label():
    composed = unicodedata.normalize("NFC", "Kompäkt")
    decomposed = unicodedata.normalize("NFD", composed)
    assert composed != decomposed
    record = _record([_filed(2021, label=decomposed)])
    assert label_filing.years_filed(record, composed) == frozenset({"2021"})
    record = _record([_filed(2021, label=composed)])
    assert label_filing.years_filed(record, decomposed) == frozenset({"2021"})


def test_a_label_is_compared_exactly_otherwise():
    record = _record([_filed(2021, label="kompakt"), _filed(2022, label="Kompakt ")])
    assert label_filing.years_filed(record, LABEL) == frozenset()


def test_a_year_is_four_digits_as_the_ledger_spells_it():
    record = _record([_filed(987), _filed(2021, tracks=3)])
    assert label_filing.years_filed(record, LABEL) == frozenset({"0987", "2021"})


# ═══════════════════════════════════════════════════════════════════════════
# 5. A real native landing, then the mark
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def landed_natively(native_library, monkeypatch):
    """The native landing suite's machine, ready to land; then ``follow`` switches
    the labels module on, follows Kompakt, builds its years on a fake account."""
    cfg, _root = native_library

    def follow() -> outbound_fakes.StrictAccount:
        full = dataclasses.replace(cfg, profile=config.ProfileConfig(name="full"))
        config.save(full)
        config.reset_cache()
        register(LABEL)
        monkeypatch.setattr(catalogue, "resolve", catalogue_factory(_catalogue()))
        account = outbound_fakes.StrictAccount()
        bind_account(monkeypatch, account)
        assert _build()[0] == int(ExitCode.OK)
        return account

    return cfg, follow


def test_a_label_batch_landed_natively_with_label_is_marked_by_its_pass(
    landed_natively, silence
):
    cfg, follow = landed_natively
    _dated(cfg, silence, "One.flac", "2021-03-01")
    _dated(cfg, silence, "Two.flac", "2023-05-01")
    code, acted, _ = _land_two_acts(_land("--label", LABEL, "--pass", PASS))
    assert code == int(ExitCode.OK), acted
    account = follow()

    code, done = _mark()

    assert code == int(ExitCode.OK), done
    assert sorted(account.renamed) == [
        ("pl-1", "DOWNLOADED Kompakt 2021"),
        ("pl-3", "DOWNLOADED Kompakt 2023"),
    ]
    reasons = {item["id"]: item.get("reason") for item in done["data"]["items"]}
    assert reasons["pl-2"] == label_mark_cli.NOT_IN_BATCH


def test_a_label_batch_landed_natively_with_a_manifest_is_marked_by_its_pass(
    landed_natively, silence, tmp_path
):
    cfg, follow = landed_natively
    for name in ("One.flac", "Two.flac"):
        _stage(cfg, silence, name)
    manifest = _manifest(
        tmp_path,
        [("1", "Probe", "One", LABEL, 2022), ("2", "Probe", "Two", "Another Label", 2023)],
    )
    code, acted, _ = _land_two_acts(_land("--manifest", str(manifest), "--pass", PASS))
    assert code == int(ExitCode.OK), acted
    account = follow()

    code, done = _mark()

    assert code == int(ExitCode.OK), done
    assert account.renamed == [("pl-2", "DOWNLOADED Kompakt 2022")]


def test_the_gate_digest_names_the_landings(native_followed):
    """What makes a second landing another plan, read off the payload itself."""
    cfg, _fake, _account = native_followed
    _record_landing(cfg, _filed(2021))
    code, first = drive(["label", "mark", LABEL, "--pass", PASS])
    assert code == int(ExitCode.DECISION_REQUIRED), first
    _record_landing(cfg, _filed(2021), stamp="130000")
    code, second = drive(["label", "mark", LABEL, "--pass", PASS])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]

