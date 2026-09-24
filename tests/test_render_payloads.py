"""R-678: the renderer's job and import proof cases, and the gates that bound them.

The verbs themselves are driven in human mode beside their own fixtures, in
``tests/intake/test_workers.py``, ``tests/test_acquire_workers.py``,
``tests/test_tag_workers.py`` and ``tests/test_intake_imported.py``. This file
holds what a verb cannot reach: a payload of the right schema from a verb the
case was not written for, and the dispatcher's refusal to name a second driver.
"""

from __future__ import annotations

import pytest

from cratekit import cli
from cratekit.cli import output, render
from cratekit.core import config, jobs
from tests.cli_drive import drive_human
from tests.test_config import valid_data

STARTED = "2026-09-23T00:00:00+00:00"


def envelope(verb: str, schema: str, data: dict) -> output.Envelope:
    return output.build(
        verb=verb, run_id="r", schema=output.current_schema(schema), started=STARTED, data=data
    )


def job_state(verb: str = "tag.folder", **data) -> output.Envelope:
    payload = {"job_id": "j-1", "state": "queued", "cause": None, "progress": {}}
    payload.update(data)
    return envelope(verb, "job_state", payload)


def test_a_queued_job_names_its_drive_only_when_one_is_handed_in():
    """The drive command comes from the dispatcher; without it no command is guessed."""
    bare = render.render_job_state(job_state())
    driven = render.render_job_state(job_state(), drive=["tag", "folder", "/x y", "--job", "j-1"])

    assert "  job: j-1, queued" in bare
    assert not any(line.startswith("  drive it with:") for line in bare)
    assert "  drive it with: crate tag folder '/x y' --job j-1" in driven


def test_a_job_that_is_not_queued_names_no_drive_even_when_handed_one():
    lines = render.render_job_state(job_state(state="running"), drive=["tag", "folder", "x"])
    assert not any(line.startswith("  drive it with:") for line in lines)


def test_an_empty_job_id_is_a_queue_that_held_nothing_and_renders_nothing():
    assert render.render_job_state(job_state(job_id="", state="no-tracks")) == []


def test_the_job_case_is_gated_on_the_schema_not_a_job_id_key():
    diagnostic = envelope(
        "intake.missing", "diagnostic", {"checks": [], "summary": {"job_id": "j-1"}}
    )
    assert render.render_job_state(diagnostic) == []


def test_the_resolution_counts_belong_to_the_intake_verbs_alone():
    """Another job_state verb whose progress happened to carry the words is not a resolution."""
    counts = {"owned": 1, "offered": 0, "missing": 2, "suppressed": 0, "total": 3, "settled": 3}
    tagged = render.render_job_state(job_state(state="succeeded", progress=counts))
    intake = render.render_job_state(
        job_state(verb="intake.playlist", state="succeeded", progress=counts)
    )

    assert not any(line.startswith("  owned:") for line in tagged)
    assert "  owned: 1 already in the library" in intake
    assert "  next: crate intake missing --job j-1" in intake


def test_a_resolution_word_the_progress_does_not_carry_is_not_printed_as_zero():
    lines = render.render_job_state(
        job_state(verb="intake.set", state="succeeded", progress={"owned": 3, "missing": 0})
    )
    assert "  owned: 3 already in the library" in lines
    assert not any(line.startswith("  offered:") for line in lines)
    assert not any(line.startswith("  next:") for line in lines)


def test_the_import_proof_is_gated_on_the_verb_as_well_as_the_schema():
    """Every planning verb answers plan/1 and only this one's items carry an action."""
    items = [{"session_id": "s", "action": "imported", "count": 2, "retired_to": "/a/f.xml.imported"}]
    plan = {"digest": "d", "items": items, "totals": {}, "chunk": None}

    assert render.render_import_proof(envelope("profile.set", "plan", plan)) == []
    lines = render.render_import_proof(envelope("intake.imported", "plan", plan))
    assert "  run s: proven imported, 2 track(s); intake file retired to f.xml.imported" in lines
    assert "  proven: 1 run(s), 2 track(s); retired: 1 intake file(s)" in lines


@pytest.mark.parametrize(
    ("item", "said"),
    [
        (
            {"session_id": "s", "action": "imported", "count": 1, "retired_to": None},
            "  run s: proven imported, 1 track(s); no intake file to retire",
        ),
        (
            {"session_id": "s", "action": "unverifiable", "why": "nothing recorded"},
            "  run s: not verifiable, nothing recorded",
        ),
        (
            {"session_id": "s", "action": "retired", "retired_to": "/a/g.xml.imported", "closed": True},
            "  run s: proven earlier; intake file retired to g.xml.imported; run closed",
        ),
        (
            {"session_id": "s", "action": "something-new"},
            "  session_id=s, action=something-new",
        ),
    ],
)
def test_each_proof_action_is_worded_and_an_unknown_one_keeps_its_fields(item, said):
    plan = {"digest": "d", "items": [item], "totals": {}, "chunk": None}
    assert said in render.render_import_proof(envelope("intake.imported", "plan", plan))


def test_a_verb_showing_a_queued_job_it_did_not_queue_names_no_drive(tmp_path, monkeypatch):
    """``job show`` and ``job resume`` answer with a queued job too, and must not name a
    second driver for it. Driven through the dispatcher, because the check lives there."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    built = config.from_dict(valid_data(tmp_path))
    config.save(built)
    config.reset_cache()
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="tag.folder",
            payload={"folder": str(tmp_path)},
            cfg=built,
            item_ids=("a.flac",),
        )

    code, text = drive_human(["job", "show", job.job_id])

    assert code == 0, text
    assert f"  job: {job.job_id}, queued" in text.splitlines(), text
    assert "drive it with" not in text, text
    assert cli._drive_argv(job_state(verb="tag.folder", job_id=job.job_id)) == [
        "tag", "folder", str(tmp_path), "--job", job.job_id,
    ]


def test_a_job_the_queue_cannot_find_falls_back_to_the_generic_resume(tmp_path, monkeypatch):
    """A refused lookup is not a failed verb: the job was queued, so a true command is named."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    config.save(config.from_dict(valid_data(tmp_path)))
    config.reset_cache()

    assert cli._drive_argv(job_state(job_id="no-such")) == ["job", "resume", "no-such"]
