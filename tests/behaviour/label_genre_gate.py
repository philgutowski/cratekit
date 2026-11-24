"""The label genre gate's scenarios: releases held, listed, returned and judged (U308)."""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_label_genre_gate import Lookup, bind, bind_lookup, isrc, provider_of
from tests.test_label_genre_gate import installed as installed  # noqa: PLC0414
from tests.test_label_judge import queue_release
from tests.test_label_workers import queued_sweep

OK = int(ExitCode.OK)
BY_LABEL = ("review", "list", "--queue", "label-release", "--group-by", "label")


def test_a_sweep_holds_what_the_gate_judges_and_held_returns_it(stage, installed, monkeypatch):
    assert stage.crate("label", "registry", "add", "Tide Works").code == OK
    bind(
        monkeypatch,
        {"r-dance": ("2026", isrc(1)), "r-christian": ("2025", isrc(2)), "r-unknown": ("2024", isrc(3))},
    )
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Dance", "Pop"), isrc(2): ("Christian",)}))
    assert stage.crate("sync", "labels", "--job", queued_sweep()).code == OK
    assert stage.crate(*BY_LABEL).code == OK
    assert stage.crate("label", "held").code == OK
    assert stage.json("label", "held").code == OK
    assert stage.crate("label", "held", "return").code != OK
    assert stage.crate("label", "held", "list", "r-christian").code != OK
    assert stage.crate("label", "held", "return", "r-christian", "r-typo").code != OK
    assert stage.crate("label", "held", "return", "r-christian").code == OK
    assert stage.crate("label", "held", "return", "r-christian").code == OK
    # A second sweep asks nobody anything, and nothing is held.
    assert stage.crate("sync", "labels", "--job", queued_sweep()).code == OK
    assert stage.crate("label", "held").code == OK


def test_judge_holds_a_waiting_release_of_another_kind(stage, installed, monkeypatch):
    assert stage.crate("label", "registry", "add", "Tide Works").code == OK
    queue_release(installed, "r-christian")
    queue_release(installed, "r-dance")
    queue_release(installed, "r-unknown")
    provider_of(monkeypatch, {"r-christian": isrc(1), "r-dance": isrc(2), "r-unknown": isrc(3)})
    bind_lookup(monkeypatch, Lookup({isrc(1): ("Christian",), isrc(2): ("Dance",)}))
    queued = stage.json("label", "judge")
    assert queued.code == OK, queued.stdout
    judged = stage.crate("label", "judge", "--job", queued.envelope["data"]["job_id"])
    assert judged.code == OK, judged.stderr
    assert stage.crate("label", "held").code == OK
    assert stage.crate(*BY_LABEL).code == OK
