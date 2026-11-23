"""U341: ``label sync --genre`` asks only the labels of one genre group, and
``label registry list --genre`` lists that group."""

from __future__ import annotations

import pytest

from cratekit.core.exit_codes import ExitCode
from cratekit.label import registry as labels
from tests.cli_drive import drive
from tests.test_label_sync import (
    bind,
    checks,
    line_for,
    next_ok,
    record,
    refused_with,
    register,
    script,
    sync,
    walked,
)
from tests.test_label_sync import installed as installed  # noqa: PLC0414 - fixture
from tests.test_label_sync import no_disk_flush as no_disk_flush  # noqa: PLC0414 - fixture

DEEP = "Deep House"
#: The followed labels in registry order, each with its genre or None.
FOLLOWED = (
    ("Alpha Works", DEEP),
    ("Beta Works", "Rominimal"),
    ("Gamma Works", None),
    ("Delta Works", DEEP),
    ("Epsilon Works", DEEP),
)


def grouped(monkeypatch, followed=FOLLOWED):
    """Every label of ``followed`` registered with its genre, two new releases each."""
    for name, genre in followed:
        if genre is None:
            register(name)
        else:
            register(name, "--genre", genre)
    return bind(monkeypatch, {
        labels.slug(name): [(f"{labels.slug(name)}-r{n}", str(2026 - n), 2) for n in range(2)]
        for name, _ in followed
    })


def registry_list(*argv: str, code: ExitCode = ExitCode.OK) -> dict:
    got, envelope = drive(["label", "registry", "list", *argv])
    assert got == int(code), envelope
    return envelope


# 1. The walk asks the group alone


def test_a_walk_with_a_genre_asks_only_that_group_in_registry_order(installed, monkeypatch):
    fake = grouped(monkeypatch)
    terminal = script(monkeypatch, "all", "not-now", "all")
    code, envelope = sync("--genre", DEEP)
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    assert fake.asked_for == ["alpha-works", "delta-works", "epsilon-works"]
    assert "Beta Works" not in terminal.shown and "Gamma Works" not in terminal.shown
    held = record(installed)
    assert [(one["label_id"], one["answer"]) for one in held["answers"]] == [
        ("alpha-works", "all"), ("delta-works", "not-now"), ("epsilon-works", "all"),
    ]
    assert sorted(held["labels"]) == ["alpha-works", "delta-works", "epsilon-works"]
    lines = envelope["cause"]["detail"]["shown"]["answered_this_run"]
    assert lines[-1] == "3 label(s) answered; every label of genre 'Deep House' is answered"
    assert not any("asking only" in one for one in lines), lines
    assert not any("calls to the streaming provider" in one for one in lines), lines


def test_a_walk_with_a_genre_names_the_group_and_estimates_it_alone(installed, monkeypatch):
    grouped(monkeypatch)
    script(monkeypatch, "quit")
    code, envelope = sync("--genre", DEEP)
    assert code == int(ExitCode.OK), envelope
    (said,) = checks(envelope, "genre")
    assert said["detail"] == (
        "asking only the 3 of 5 followed label(s) of genre 'Deep House': "
        "Alpha Works, Delta Works, Epsilon Works"
    )
    (estimate,) = checks(envelope, "estimate")
    assert "over 3 labels" in estimate["detail"], estimate


def test_a_walk_without_a_genre_asks_every_label_and_names_no_group(installed, monkeypatch):
    fake = grouped(monkeypatch)
    script(monkeypatch, *(["not-now"] * len(FOLLOWED)))
    lines = walked()
    assert fake.asked_for == [labels.slug(name) for name, _ in FOLLOWED]
    assert lines[-1] == "5 label(s) answered; every label is answered"


def test_the_genre_is_matched_whatever_its_case(installed, monkeypatch):
    fake = grouped(monkeypatch)
    script(monkeypatch, "quit")
    code, envelope = sync("--genre", "  deep HOUSE ")
    assert code == int(ExitCode.OK), envelope
    assert fake.asked_for == ["alpha-works"]
    assert "of genre 'Deep House':" in checks(envelope, "genre")[0]["detail"]


# 2. The run after quit resumes inside the group


def test_the_walk_after_quit_resumes_inside_the_group(installed, monkeypatch):
    fake = grouped(monkeypatch)
    script(monkeypatch, "all", "quit")
    code, envelope = sync("--genre", DEEP)
    assert code == int(ExitCode.OK), envelope
    summary = envelope["data"]["summary"]
    assert summary["stopped_at"] == "delta-works"
    (run_line,) = checks(envelope, "run")
    assert run_line["detail"] == (
        "1 label(s) answered; stopped at delta-works, run label sync --genre "
        "'Deep House' again to go on"
    )
    assert fake.asked_for == ["alpha-works", "delta-works"]
    script(monkeypatch, "pick", "1", "stop")
    lines = walked_with("--genre", DEEP)
    assert fake.asked_for[2:] == ["alpha-works", "delta-works", "epsilon-works"]
    assert "nothing new" in line_for(lines, "Alpha Works")
    assert line_for(lines, "Delta Works").startswith("Delta Works: pick")
    held = record(installed)
    assert [(one["label_id"], one["answer"]) for one in held["answers"]] == [
        ("alpha-works", "all"), ("delta-works", "pick"), ("epsilon-works", "stop"),
    ]
    assert "beta-works" not in held["labels"] and "gamma-works" not in held["labels"]
    assert "epsilon-works" not in labels.RegistryStore().load().labels


def walked_with(*argv: str) -> list[str]:
    code, envelope = sync(*argv)
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    return envelope["cause"]["detail"]["shown"]["answered_this_run"]


# 3. --next with a genre


def test_next_with_a_genre_asks_the_first_label_of_the_group(installed, monkeypatch):
    fake = grouped(monkeypatch)
    envelope = next_ok("--genre", "Rominimal")
    assert envelope["data"]["summary"]["question"]["label_id"] == "beta-works"
    assert fake.asked_for == ["beta-works"]
    assert "of genre 'Rominimal': Beta Works" in checks(envelope, "genre")[0]["detail"]
    assert "over 1 label," in checks(envelope, "estimate")[0]["detail"]


def test_next_with_a_genre_leaves_a_question_saved_outside_the_group(installed, monkeypatch):
    fake = grouped(monkeypatch)
    assert next_ok()["data"]["summary"]["question"]["label_id"] == "alpha-works"
    shown = next_ok("--genre", "Rominimal")["data"]["summary"]["question"]
    assert shown["label_id"] == "beta-works"
    assert fake.asked_for == ["alpha-works", "beta-works"]
    held = record(installed)["labels"]
    assert held["alpha-works"]["pending"] and held["beta-works"]["pending"]
    again = next_ok("--genre", DEEP)["data"]["summary"]["question"]
    assert again["label_id"] == "alpha-works"
    assert fake.asked_for == ["alpha-works", "beta-works"], "a saved question is not listed again"


def test_next_with_a_genre_whose_labels_have_nothing_new_says_so_of_the_group(
    installed, monkeypatch
):
    for name, genre in FOLLOWED:
        register(name, *(("--genre", genre) if genre else ()))
    bind(monkeypatch, {labels.slug(name): [] for name, _ in FOLLOWED})
    envelope = next_ok("--genre", DEEP)
    assert envelope["data"]["summary"]["question"] is None
    (said,) = checks(envelope, "question")
    assert said["detail"] == "no label of genre 'Deep House' has anything new to ask about"


# 4. Refusals


def test_a_genre_the_taxonomy_does_not_declare_refuses_naming_the_carried_genres(
    installed, monkeypatch
):
    fake = grouped(monkeypatch)
    envelope = refused_with("label-unknown", "--genre", "Polka")
    message = envelope["cause"]["message"]
    assert "'Polka'" in message
    assert "taxonomy declares no bucket for it but its fallback" in message
    assert "the followed labels carry Deep House, Rominimal" in message
    assert envelope["cause"]["detail"] == {"genre": "Polka", "genres": [DEEP, "Rominimal"]}
    assert fake.asked_for == []
    assert record(installed)["labels"] == {}


def test_a_declared_genre_no_label_carries_refuses_as_a_group_of_none(installed, monkeypatch):
    fake = grouped(monkeypatch)
    envelope = refused_with("label-unknown", "--next", "--genre", "Minimal Techno")
    message = envelope["cause"]["message"]
    assert "no followed label carries the genre 'Minimal Techno', so" in message
    assert "fallback" not in message
    assert envelope["cause"]["detail"]["genres"] == [DEEP, "Rominimal"]
    assert fake.asked_for == []


def test_a_genre_asked_of_labels_that_carry_none_says_how_to_set_one(installed, monkeypatch):
    grouped(monkeypatch, (("Alpha Works", None), ("Beta Works", None)))
    envelope = refused_with("label-unknown", "--genre", DEEP)
    assert "no followed label carries a genre; set one with" in envelope["cause"]["message"]
    assert envelope["cause"]["detail"]["genres"] == []


def test_a_genre_with_no_labels_followed_refuses_as_an_empty_registry(installed, monkeypatch):
    refused_with("label-registry-empty", "--genre", DEEP)


def test_an_empty_genre_refuses_as_a_shapeless_one(installed, monkeypatch):
    grouped(monkeypatch)
    refused_with("label-name-invalid", "--genre", " ")


@pytest.mark.parametrize("argv", [
    ("--go",),
    ("--answer", "all", "--label", "Alpha Works"),
    ("--next", "--label", "Alpha Works"),
])
def test_a_genre_beside_go_answer_or_one_label_refuses_as_a_selection(
    installed, monkeypatch, argv
):
    fake = grouped(monkeypatch)
    envelope = refused_with("review-selection-invalid", "--genre", DEEP, *argv)
    assert "--genre chooses the labels" in envelope["cause"]["message"]
    assert fake.asked_for == []
    assert record(installed)["labels"] == {}


# 5. The registry lists one group


def test_registry_list_with_a_genre_lists_that_group_alone(installed, monkeypatch):
    grouped(monkeypatch)
    envelope = registry_list("--genre", "deep house")
    summary = envelope["data"]["summary"]
    assert summary["genre"] == DEEP
    assert summary["count"] == 3 and summary["registered"] == 5
    assert [one["label_id"] for one in summary["labels"]] == [
        "alpha-works", "delta-works", "epsilon-works",
    ]
    assert [one["key"] for one in envelope["data"]["checks"]] == [
        "labels.alpha-works", "labels.delta-works", "labels.epsilon-works",
    ]


def test_registry_list_without_a_genre_lists_every_label(installed, monkeypatch):
    grouped(monkeypatch)
    summary = registry_list()["data"]["summary"]
    assert summary["count"] == 5 and "genre" not in summary


def test_registry_list_with_a_genre_no_label_carries_refuses(installed, monkeypatch):
    grouped(monkeypatch)
    envelope = registry_list("--genre", "Polka", code=ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "label-unknown"
    assert envelope["cause"]["detail"]["genres"] == [DEEP, "Rominimal"]


@pytest.mark.parametrize("extra", [("--kind", "any"), ("--accept-fallback",), ("--offer", "3")])
def test_registry_list_takes_a_genre_and_no_field_to_set(installed, monkeypatch, extra):
    grouped(monkeypatch)
    envelope = registry_list("--genre", DEEP, *extra, code=ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "label-name-invalid"
    assert "--genre alone" in " ".join(envelope["cause"]["remediation"]["steps"])


def test_registry_remove_still_refuses_a_genre(installed, monkeypatch):
    grouped(monkeypatch)
    got, envelope = drive(["label", "registry", "remove", "Alpha Works", "--genre", DEEP])
    assert got == int(ExitCode.PRECONDITION), envelope
    assert "alpha-works" in labels.RegistryStore().load().labels


# 6. The registry's group, as data


def test_a_group_is_matched_folded_and_each_genre_named_once_as_first_spelled():
    held = labels.Registry(labels={
        entry.label_id: entry for entry in (
            labels.LabelEntry(label_id="a", name="A", genre="Deep House"),
            labels.LabelEntry(label_id="b", name="B"),
            labels.LabelEntry(label_id="c", name="C", genre="deep house"),
            labels.LabelEntry(label_id="d", name="D", genre="Rominimal"),
        )
    })
    assert [one.label_id for one in held.of_genre("DEEP HOUSE")] == ["a", "c"]
    assert held.of_genre("Deep") == ()
    assert held.genres() == ("Deep House", "Rominimal")
