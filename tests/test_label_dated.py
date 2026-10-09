"""U117: new label releases kept apart from the ones already heard.

Each scenario the brief names, narrowed by the watcher's two answers to the
account half: the label review store is the record of what a go took and of
what was heard, the dated playlist is planned by ``crate organize``'s account
step beside the year playlist, and the year playlist is left as it was. The
account and the catalogue are the suite's fakes. Nothing here names a real
volume, a real person or a real track.
"""

from __future__ import annotations

import ast
import dataclasses
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.label import dated, playlists_cli, sync_cli
from cratekit.modules.outbound import folders
from cratekit.organize import account as organize_account
from cratekit.organize.steps import NOTHING, PLANNED, REFUSED, Area
from tests.test_label_playlists import LABEL, LABEL_ID, _entry, _years
from tests.test_label_playlists import followed as followed  # noqa: PLC0414 - fixture
from tests.test_label_workers import installed as installed  # noqa: PLC0414 - fixture

TODAY = date(2026, 10, 9)


def _instant(day: str, hour: int = 12) -> str:
    """Noon local on ``day``, recorded the way ``settle_in`` records it, in UTC."""
    local = datetime.fromisoformat(f"{day}T{hour:02d}:00:00").astimezone()
    return local.astimezone(timezone.utc).isoformat()


def _answer(taken: list[str], day: str, *, answer: str = sync_cli.ALL, settled: bool = True):
    entry = {
        "label_id": LABEL_ID,
        "label_name": LABEL,
        "answer": answer,
        "answered_at": _instant(day, 9),
        "taken": list(taken),
        "releases": [{"identity": one} for one in taken],
    }
    if settled:
        entry[sync_cli.SETTLED] = {"run": "go-1", "at": _instant(day)}
    return entry


def _record(cfg, answers, heard=None) -> None:
    labels = {LABEL_ID: {"asked": []}}
    if heard is not None:
        labels[LABEL_ID][dated.HEARD] = list(heard)
    sync_cli.write_record(
        cfg, {"version": sync_cli.RECORD_VERSION, "labels": labels, "answers": list(answers)}
    )


def _built(cfg, fake, account) -> folders.Plan:
    """The label's year playlists built as ``label playlists`` builds them."""
    year_plan = playlists_cli.plan_label(cfg, _entry(), fake, account)
    playlists_cli.apply_plan(cfg, account, year_plan)
    return playlists_cli.plan_label(cfg, _entry(), fake, account)


def _plan(cfg, fake, account, *, today=TODAY) -> dated.DatedPlan:
    year_plan = playlists_cli.plan_label(cfg, _entry(), fake, account)
    return dated.plan(
        cfg,
        year_plan.catalogue,
        year_plan.folder_id,
        account,
        sync_cli.load_record(cfg),
        today=today,
    )


# 1. The record read


def test_the_go_day_is_the_local_day_of_the_settling():
    document = {"answers": [_answer(["r3"], "2026-10-08")], "labels": {}}
    assert dated.taken_by_goes(document, LABEL_ID) == {"r3": "2026-10-08"}


def test_an_unsettled_or_not_now_answer_took_nothing():
    document = {
        "labels": {},
        "answers": [
            _answer(["r3"], "2026-10-08", settled=False),
            _answer(["r4"], "2026-10-08", answer=sync_cli.NOT_NOW),
        ],
    }
    assert dated.taken_by_goes(document, LABEL_ID) == {}


def test_an_absent_heard_list_is_nothing_heard():
    assert dated.heard({"labels": {LABEL_ID: {}}}, LABEL_ID) == frozenset()
    assert dated.heard({"labels": {}}, LABEL_ID) == frozenset()
    assert dated.heard({"labels": {LABEL_ID: {"heard": ["r3", 4]}}}, LABEL_ID) == {"r3"}


def test_the_name_is_the_year_name_then_new_then_the_day():
    assert dated.dated_name(LABEL, "2023", "2026-10-09") == "Kompakt 2023 new 2026-10-09"


# 2. A go into a year that exists


def test_a_go_into_an_existing_year_makes_a_dated_playlist_and_leaves_the_year(followed):
    cfg, fake, account = followed
    year_plan = _built(cfg, fake, account)
    (folder_id,) = account.folder_names
    before = _years(account, folder_id)
    assert "Kompakt 2023" in before
    _record(cfg, [_answer(["r3"], "2026-10-09")])

    planned = _plan(cfg, fake, account)
    assert [(s.name, s.action, s.add) for s in planned.steps] == [
        ("Kompakt 2023 new 2026-10-09", dated.CREATE, ("t4", "t5"))
    ]
    dated.apply(cfg, account, planned)

    after = _years(account, folder_id)
    assert after["Kompakt 2023 new 2026-10-09"] == ["t4", "t5"]
    assert {k: v for k, v in after.items() if " new " not in k} == before
    assert not year_plan.writes


def test_a_second_go_the_same_day_appends_to_the_same_dated_playlist(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    (folder_id,) = account.folder_names
    _record(cfg, [_answer(["r3"], "2026-10-09")])
    dated.apply(cfg, account, _plan(cfg, fake, account))

    _record(cfg, [_answer(["r3"], "2026-10-09"), _answer(["r4"], "2026-10-09")])
    planned = _plan(cfg, fake, account)
    assert [(s.action, s.add) for s in planned.steps] == [(dated.REUSE, ("t6", "t7"))]
    dated.apply(cfg, account, planned)

    held = _years(account, folder_id)
    assert held["Kompakt 2023 new 2026-10-09"] == ["t4", "t5", "t6", "t7"]
    assert sum(1 for title in account.titles.values() if " new " in title) == 1
    assert not _plan(cfg, fake, account).writes


def test_a_go_on_another_day_makes_its_own_dated_playlist(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r3"], "2026-10-08"), _answer(["r4"], "2026-10-09")])
    names = [step.name for step in _plan(cfg, fake, account).steps]
    assert names == ["Kompakt 2023 new 2026-10-08", "Kompakt 2023 new 2026-10-09"]


def test_a_heard_release_is_left_out_and_the_record_is_not_written(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r3", "r4"], "2026-10-09")], heard=["r3"])
    path = config.state_path("label_sync", cfg)
    before = path.read_bytes()
    planned = _plan(cfg, fake, account)
    assert [s.add for s in planned.steps] == [("t6", "t7")]
    assert planned.left_out == {"heard": 1}
    dated.apply(cfg, account, planned)
    assert path.read_bytes() == before


def test_a_release_the_catalogue_does_not_confirm_is_left_out(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r6", "r5"], "2026-10-09")])
    planned = _plan(cfg, fake, account)
    assert planned.steps == ()
    assert planned.left_out == {"not in the catalogue": 1, "undated": 1}


def test_two_playlists_with_the_dated_name_are_left_alone(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    (folder_id,) = account.folder_names
    for _ in range(2):
        account.move_to_folder(account.create_playlist("Kompakt 2023 new 2026-10-09"), folder_id)
    _record(cfg, [_answer(["r3"], "2026-10-09")])
    (step,) = _plan(cfg, fake, account).steps
    assert step.action == dated.AMBIGUOUS and not step.writes


# 3. The age report


def test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r3"], "2026-09-01"), _answer(["r4"], "2026-10-01")])
    dated.apply(cfg, account, _plan(cfg, fake, account, today=date(2026, 9, 2)))
    writes = len(account.chunks), len(account.moves), len(account.created)

    planned = _plan(cfg, fake, account)
    assert [(one.name, one.days) for one in planned.aged] == [
        ("Kompakt 2023 new 2026-09-01", 38)
    ]
    assert not planned.writes
    dated.apply(cfg, account, planned)
    assert (len(account.chunks), len(account.moves), len(account.created)) == writes
    (item,) = [one for one in planned.items() if one["action"] == "report"]
    assert "never merged" in item["why"] and "30" in item["why"]


def test_the_age_is_the_configured_one(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    _record(cfg, [_answer(["r3"], "2026-10-01")])
    dated.apply(cfg, account, _plan(cfg, fake, account))
    assert _plan(cfg, fake, account).aged == ()
    tight = dataclasses.replace(cfg, labels=config.LabelsConfig(new_playlist_age_days=7))
    assert [one.days for one in _plan(tight, fake, account).aged] == [8]


def test_the_age_key_defaults_to_thirty_and_refuses_zero():
    assert config.DEFAULT_NEW_PLAYLIST_AGE_DAYS == 30
    assert config.LabelsConfig().new_playlist_age_days == 30
    problems = config._validate_labels({"labels": {"new_playlist_age_days": 0}})
    assert problems and "labels.new_playlist_age_days" in problems[0]
    assert config._validate_labels({"labels": {"new_playlist_age_days": 14}}) == []


# 4. The account refusing part way


def test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes(followed):
    cfg, fake, account = followed
    _built(cfg, fake, account)
    (folder_id,) = account.folder_names
    _record(cfg, [_answer(["r1"], "2026-10-08"), _answer(["r3"], "2026-10-09")])
    planned = _plan(cfg, fake, account)
    assert [s.name for s in planned.steps] == [
        "Kompakt 2021 new 2026-10-08",
        "Kompakt 2023 new 2026-10-09",
    ]
    account.fail_on = frozenset({"Kompakt 2023 new 2026-10-09"})
    with pytest.raises(CratekitError) as raised:
        dated.apply(cfg, account, planned)
    cause = raised.value.cause
    assert "1 dated playlist(s) were created and 2 track(s) added" in cause.message
    assert cause.detail["created"] == ["Kompakt 2021 new 2026-10-08"]

    account.fail_on = frozenset()
    again = _plan(cfg, fake, account)
    assert [(s.action, s.add) for s in again.steps] == [
        (dated.REUSE, ()),
        (dated.CREATE, ("t4", "t5")),
    ]
    dated.apply(cfg, account, again)
    held = _years(account, folder_id)
    assert held["Kompakt 2021 new 2026-10-08"] == ["t1", "t2"]
    assert held["Kompakt 2023 new 2026-10-09"] == ["t4", "t5"]


def test_a_label_with_no_folder_yet_refuses_the_apply_before_any_write(followed):
    cfg, fake, account = followed
    _record(cfg, [_answer(["r3"], "2026-10-09")])
    planned = _plan(cfg, fake, account)
    assert planned.folder_id == "" and planned.writes
    with pytest.raises(CratekitError) as raised:
        dated.apply(cfg, account, planned)
    assert raised.value.cause.reason == "label-new-playlists-no-folder"
    assert account.created == []


# 5. The organize step


def _organize(cfg) -> Area:
    return organize_account.plan_area(
        cfg, available=frozenset({"labels"}), followed=[_entry()]
    )


def _step(area: Area):
    (step,) = [one for one in area.steps if one.key == f"label-new:{LABEL_ID}"]
    return step


def test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order(followed):
    cfg, _fake, account = followed
    _record(cfg, [_answer(["r3"], "2026-10-09")])
    area = _organize(cfg)
    keys = [one.key for one in area.steps]
    assert keys.index(f"label-new:{LABEL_ID}") == keys.index(f"label:{LABEL_ID}") + 1
    step = _step(area)
    assert step.state == PLANNED and step.counts["add"] == 2
    for one in area.steps:
        if one.apply is not None and one.key.startswith("label"):
            one.applied = one.apply()
    (folder_id,) = account.folder_names
    held = _years(account, folder_id)
    assert held["Kompakt 2023"] == ["t4", "t5", "t6", "t7"]
    assert held["Kompakt 2023 new 2026-10-09"] == ["t4", "t5"]


def test_organize_with_nothing_taken_plans_nothing(followed):
    cfg, _fake, _account = followed
    step = _step(_organize(cfg))
    assert step.state == NOTHING and step.apply is None


def test_an_unreadable_record_refuses_the_dated_step_alone(followed):
    cfg, _fake, _account = followed
    path = config.state_path("label_sync", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    area = _organize(cfg)
    assert _step(area).state == REFUSED
    assert next(one for one in area.steps if one.key == f"label:{LABEL_ID}").state == PLANNED


# 6. Add only


def test_no_removal_shape_appears_in_the_dated_module():
    shapes = ("remove", "delete", "unheart", "unlike", "clear", "rename")
    source = Path(dated.__file__).read_text(encoding="utf-8")
    named = sorted(
        {
            node.attr if isinstance(node, ast.Attribute) else node.name
            for node in ast.walk(ast.parse(source))
            if (isinstance(node, ast.Attribute) and any(s in node.attr.lower() for s in shapes))
            or (isinstance(node, ast.FunctionDef) and any(s in node.name.lower() for s in shapes))
        }
    )
    assert named == [], named
