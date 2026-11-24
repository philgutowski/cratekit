"""Label sync's scenarios: the questions asked label by label, answered, and refused (U308).

Through the structured path and a scripted terminal whose words are printed,
so the questions are held in order. Nothing is downloaded.
"""

from __future__ import annotations

from cratekit.cli import prompt
from cratekit.core.exit_codes import ExitCode
from cratekit.label import sync_cli
from tests.test_label_sync import Scripted, bind
from tests.test_label_sync import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
SYNC = ("label", "sync")


def _terminal(monkeypatch, *answers: str) -> None:
    """The suite's scripted terminal, its every word printed into the command's output."""
    scripted = Scripted(list(answers))
    monkeypatch.setattr(
        sync_cli,
        "PROMPTER",
        lambda: prompt.Prompter(read_line=scripted.read_line, write=lambda text: print(text, end="")),
    )


def test_labels_in_each_state_asked_answered_and_refused(stage, installed, monkeypatch):
    for name in ("Alpha Works", "Beta Works", "Gamma Works", "Delta Works"):
        assert stage.crate("label", "registry", "add", name).code == OK
    bind(
        monkeypatch,
        {
            "alpha-works": [("a3", "2026", 4), ("a2", "2025", 2), ("a1", "2024", 1)],
            "beta-works": [],
            "gamma-works": [("g2", "2026", 2), ("g1", "2025", 3)],
            "delta-works": [("d1", "2026", 1)],
        },
    )
    # Nothing is waiting yet, so an answer is refused and records nothing.
    assert stage.crate(*SYNC, "--answer", "all", "--label", "alpha-works").code != OK
    assert stage.crate(*SYNC, "--next").code == OK
    assert stage.json(*SYNC, "--next").code == OK
    picked = stage.json(*SYNC, "--answer", "pick", "--label", "alpha-works", "--release", "a2")
    assert picked.code == OK, picked.stdout
    assert stage.crate(*SYNC, "--next", "--label", "Gamma Works").code == OK
    assert stage.crate(*SYNC, "--answer", "not-now", "--label", "gamma-works").code == OK
    # Refusals: a label nobody follows, a pick the question did not offer, a half shape.
    assert stage.crate(*SYNC, "--answer", "all", "--label", "Nobody Works").code != OK
    assert stage.crate(*SYNC, "--next", "--label", "Nobody Works").code != OK
    assert stage.crate(*SYNC, "--answer", "pick", "--label", "alpha-works").code != OK

    # At the terminal: a word outside the set is asked again, then delta is stopped.
    _terminal(monkeypatch, "maybe", "stop")
    walked = stage.crate(*SYNC)
    assert walked.code == int(ExitCode.DECISION_REQUIRED), walked.stdout
    assert stage.crate(*SYNC, "--next").code == OK
    assert stage.crate("label", "registry").code == OK


def test_a_question_nobody_answers_and_an_empty_registry_refuse(stage, installed, monkeypatch):
    bind(monkeypatch, {"tide-works": [("r2", "2026", 2), ("r1", "2025", 1)]})
    assert stage.crate(*SYNC, "--next").code != OK
    assert stage.json(*SYNC, "--next").code != OK
    assert stage.crate("label", "registry", "add", "Tide Works").code == OK
    _terminal(monkeypatch, "", "", "")
    assert stage.crate(*SYNC).code != OK
    # The saved question is printed again with no provider call.
    assert stage.crate(*SYNC, "--next").code == OK
    _terminal(monkeypatch, "pick", "9", "1")
    assert stage.crate(*SYNC).code == int(ExitCode.DECISION_REQUIRED)
