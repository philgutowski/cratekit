"""``--progress json`` streams a long verb's steps and jobs as JSON lines (U963).

An app running ``crate sync land`` under ``--output json`` reads one
``progress/1`` event per line on standard error while the pass runs, then the
envelope on standard output. Driven in process over the sync land fakes, and
in a child process over a real pipe, since a buffer or a closed reader only
shows there (R-932).
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import output, progress, sync_land
from cratekit.cli import tail as tail_chain
from cratekit.core import jobs
from cratekit.core.exit_codes import ExitCode
from tests.test_sync_land import (  # noqa: F401 - a fixture
    Tail,
    _machine,
    _model_cannot_score,
    _ready,
    _summary,
    vocal_model,
)

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "tests" / "schemas" / "progress.v1.json"
CHILD = REPO / "tests" / "_progress_child.py"
FLAGGED = ["--output", "json", "--progress", "json", "sync", "land"]


class Tape:
    """Two streams writing into one ordered record, so stderr and stdout interleave."""

    def __init__(self) -> None:
        self.record: list[tuple[str, str]] = []
        self.out = self._stream("out")
        self.err = self._stream("err")

    def _stream(self, name: str):
        record = self.record

        class Stream(io.StringIO):
            def write(self, text: str) -> int:
                if text:
                    record.append((name, text))
                return super().write(text)

        return Stream()


def _events(text: str) -> list[dict]:
    """Every event on standard error, up to and including ``end``."""
    events = []
    for line in text.splitlines():
        event = json.loads(line)
        events.append(event)
        if event["kind"] == "end":
            break
    return events


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """The slim profile, as the sync land suite's own ``machine`` builds it."""
    return _machine(tmp_path, monkeypatch, "slim")


@pytest.fixture
def tail(monkeypatch) -> Tail:
    stand_in = Tail()
    monkeypatch.setattr(tail_chain, "dispatch", stand_in)
    monkeypatch.setattr(progress, "WATCH_SECONDS", 0.01)
    return stand_in


# 1. The declaration


def test_the_event_document_is_the_committed_schema():
    assert output.progress_document() == json.loads(SCHEMA.read_text())
    assert output.PROGRESS_SCHEMA == "progress/1"
    assert "progress" not in output.schema_names()


def test_the_validator_refuses_an_unknown_kind_a_missing_field_and_an_extra_one():
    event = output.progress_event("end", verb="sync.land", run_id="r", exit_code=0)
    assert output.progress_problems(event) == []
    assert output.progress_problems({**event, "kind": "beat"}) == ["'beat' is not a declared progress kind"]
    assert output.progress_problems({k: v for k, v in event.items() if k != "exit_code"}) == [
        "missing required field 'exit_code'"
    ]
    assert output.progress_problems({**event, "token": "x"}) == ["undeclared field 'token'"]
    assert output.progress_problems({**event, "exit_code": True}) == [
        "'exit_code' should be integer, got bool"
    ]
    assert output.progress_problems({**event, "schema": "progress/2"}) == [
        "schema is 'progress/2', not 'progress/1'"
    ]


# 2. sync land under the flag, in process


def test_sync_land_streams_its_steps_in_order_each_job_then_end_then_the_envelope(
    machine, monkeypatch, tail
):
    _ready(machine, monkeypatch, "101", "102")
    tape = Tape()

    code = cli.run(FLAGGED, stdout=tape.out, stderr=tape.err)

    assert code == int(ExitCode.PENDING_HUMAN)
    envelope = json.loads(tape.out.getvalue())
    events = _events(tape.err.getvalue())
    for event in events:
        assert output.progress_problems(event) == [], event
        assert (event["verb"], event["run_id"]) == ("sync.land", envelope["run_id"])
    assert events[-1]["kind"] == "end"
    assert events[-1]["exit_code"] == code

    steps = [event for event in events if event["kind"] == "step"]
    assert {event["of"] for event in steps} == {len(sync_land.STEPS)}
    for event in steps:
        assert event["index"] == sync_land.STEPS.index(event["name"]) + 1, event
    indexes = [event["index"] for event in steps]
    assert indexes == sorted(indexes)
    assert {event["name"] for event in steps} >= {
        sync_land.PREFLIGHT, sync_land.SYNC, sync_land.DOWNLOAD, tail_chain.TAG,
        tail_chain.ANALYZE, tail_chain.RESTAMP, tail_chain.LAND,
    }
    commands = [event["command"] for event in steps if event["command"] is not None]
    assert commands == [" ".join(argv) for argv in _summary(envelope)["commands"]]

    # Every job a step drove is reported, its last event its settled state.
    with jobs.open_store() as store:
        driven = {job.job_id: job for job in jobs.list_jobs(store)}
    reported = [event for event in events if event["kind"] == "job"]
    for job_id in {argv[argv.index("--job") + 1] for argv in tail.calls if "--job" in argv}:
        own = [event for event in reported if event["job_id"] == job_id]
        assert own, job_id
        assert own[-1]["state"] == str(driven[job_id].state) == "succeeded"
        with jobs.open_store() as store:
            assert own[-1]["progress"] == jobs.progress(store, job_id)
    # A job event follows the step that drove it.
    first = events.index(reported[0])
    assert events[first - 1]["kind"] in ("step", "job")
    # The watcher writes a change, never the same reading twice in a row, but
    # always once after the drive.
    for job_id in {event["job_id"] for event in reported}:
        own = [(event["state"], event["progress"]) for event in reported if event["job_id"] == job_id]
        repeated = [one for one, two in zip(own, own[1:]) if one == two]
        assert repeated in ([], [own[-1]]), (job_id, own)

    # end is written before the envelope, which is standard output's one write.
    kinds = [(name, text) for name, text in tape.record if text.strip()]
    ended = next(i for i, (name, text) in enumerate(kinds) if '"kind":"end"' in text)
    (written,) = [i for i, (name, _text) in enumerate(kinds) if name == "out"]
    assert ended < written


def test_a_pass_continued_by_run_decide_streams_its_steps_and_jobs_as_events(
    tmp_path, monkeypatch, tail
):
    """The recorded line keeps no root options, so the continuation takes the caller's writer."""
    _ready(_machine(tmp_path, monkeypatch, "full"), monkeypatch, "101")
    _model_cannot_score(monkeypatch)
    out, err = io.StringIO(), io.StringIO()
    assert cli.run(FLAGGED, stdout=out, stderr=err) == int(ExitCode.DECISION_REQUIRED)
    stopped = json.loads(out.getvalue())
    run_id = stopped["run_id"]
    answer = [
        "--output", "json", "--progress", "json", "run", "decide", run_id,
        sync_land.WITHOUT_VOCALS, sync_land.WITHOUT_VOCALS_GO, "--continue",
    ]
    out, err = io.StringIO(), io.StringIO()

    code = cli.run(answer, stdout=out, stderr=err)

    assert code == int(ExitCode.PENDING_HUMAN)
    envelope = json.loads(out.getvalue())
    events = _events(err.getvalue())
    assert all(output.progress_problems(event) == [] for event in events)
    assert not [line for line in err.getvalue().split('{"schema"')[0].splitlines() if line]
    steps = [event for event in events if event["kind"] == "step"]
    assert {event["name"] for event in steps} >= {tail_chain.TAG, tail_chain.LAND}
    assert {(event["verb"], event["run_id"]) for event in steps} == {("sync.land", run_id)}
    assert [event for event in events if event["kind"] == "job"]
    assert events[-1]["kind"] == "end"
    assert (events[-1]["exit_code"], events[-1]["run_id"]) == (code, envelope["run_id"])


def test_end_carries_the_envelopes_run_when_the_verb_was_refused_before_its_run(
    machine, monkeypatch, tail
):
    out, err = io.StringIO(), io.StringIO()

    code = cli.run(["--output", "json", "--progress", "json", "--run", "no-such-run", "sync", "land"],
                   stdout=out, stderr=err)

    envelope = json.loads(out.getvalue())
    assert code != int(ExitCode.OK)
    (end,) = _events(err.getvalue())
    assert (end["kind"], end["exit_code"], end["run_id"]) == ("end", code, envelope["run_id"])
    assert end["run_id"]


def test_the_parser_spells_the_writers_one_value():
    assert cli.PROGRESS_JSON == progress.JSON


def test_without_the_flag_json_output_says_nothing_on_standard_error_before_the_result(
    machine, monkeypatch, tail
):
    _ready(machine, monkeypatch, "101")
    out, err = io.StringIO(), io.StringIO()

    code = cli.run(["--output", "json", "sync", "land"], stdout=out, stderr=err)

    assert code == int(ExitCode.PENDING_HUMAN)
    json.loads(out.getvalue())
    assert "step 1 of" not in err.getvalue()
    assert not [line for line in err.getvalue().splitlines() if line.startswith("{")]


def test_the_flag_in_human_output_turns_its_lines_into_events(machine, monkeypatch, tail):
    _ready(machine, monkeypatch, "101")
    out, err = io.StringIO(), io.StringIO()

    cli.run(["--progress", "json", "sync", "land"], stdout=out, stderr=err)

    lines = err.getvalue().splitlines()
    events = _events("\n".join(line for line in lines if line.startswith("{")))
    assert events and all(output.progress_problems(event) == [] for event in events)
    assert "step 1 of" not in err.getvalue()


# 3. Human output is today's


def _chained(writer) -> None:
    chain = tail_chain.Chain(
        progress=writer, namespace="x", title="sync land", steps=("one", "two"),
        origin=("x",), again="again",
    )
    chain.say("one", "a person reads this")
    chain.say("two", "crate tag folder /staged", command="crate tag folder /staged")


def test_human_progress_is_the_line_a_plain_writer_wrote():
    plain: list[str] = []
    _chained(plain.append)
    stream = io.StringIO()
    writer = progress.Writer(stream, verb="sync.land", events=False)
    _chained(writer)
    writer.job(step="two", job_id="j", state="running", progress={})
    writer.end(run_id="r", exit_code=0)
    writer("an intake line")

    assert stream.getvalue() == "".join(f"{line}\n" for line in [*plain, "an intake line"])
    assert plain == [
        "sync land, step 1 of 2, one: a person reads this",
        "sync land, step 2 of 2, two: crate tag folder /staged",
    ]


def test_a_plain_progress_line_becomes_a_line_event():
    stream = io.StringIO()
    writer = progress.Writer(stream, verb="intake.set", events=True)
    writer.run_id = "r"
    _chained(writer)
    writer("fetched 3 of 9")

    one, two, line = (json.loads(text) for text in stream.getvalue().splitlines())
    assert (one["kind"], one["index"], one["of"], one["name"]) == ("step", 1, 2, "one")
    assert (one["command"], one["detail"]) == (None, "a person reads this")
    assert (two["command"], two["detail"]) == ("crate tag folder /staged", None)
    assert (line["kind"], line["text"], line["run_id"]) == ("line", "fetched 3 of 9", "r")


@pytest.mark.parametrize("choice, as_json, expected", [
    (None, False, False), (None, True, None), ("json", True, True), ("json", False, True),
])
def test_the_writer_a_verb_is_handed(choice, as_json, expected):
    writer = progress.writer_for(choice, io.StringIO(), verb="v", as_json=as_json)
    assert (None if writer is None else writer.events) == expected


# 4. A reader that stops reading


@pytest.mark.parametrize("failure", [BrokenPipeError, ValueError])
def test_a_line_that_cannot_be_written_is_dropped(failure):
    class Closed:
        def write(self, _text):
            raise failure("closed")

        def flush(self):
            raise failure("closed")

    writer = progress.Writer(Closed(), verb="v", events=True)
    writer("dropped")
    writer.end(run_id="r", exit_code=0)


def _child(tmp_path: Path, **env: str) -> tuple[subprocess.Popen, Path]:
    result = tmp_path / "result.json"
    process = subprocess.Popen(
        [
            sys.executable, "-m", "pytest", "-o", "addopts=", "-p", "no:cacheprovider", "-s",
            "--basetemp", str(tmp_path / "child"), f"{CHILD}::test_child",
        ],
        cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        env={**os.environ, "CRATEKIT_PROGRESS_CHILD_RESULT": str(result), **env},
    )
    return process, result


def _lines(stream, into: list[str]) -> threading.Thread:
    def read() -> None:
        for raw in iter(stream.readline, b""):
            into.append(raw.decode())

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    return reader


def test_a_job_event_arrives_over_a_real_pipe_while_the_job_still_runs(tmp_path):
    go = tmp_path / "go"
    process, result = _child(tmp_path, CRATEKIT_PROGRESS_CHILD_GO=str(go))
    lines: list[str] = []
    reader = _lines(process.stderr, lines)
    deadline = time.monotonic() + 120
    running = None
    while running is None and time.monotonic() < deadline and process.poll() is None:
        for line in list(lines):
            if line.startswith("{"):
                event = json.loads(line)
                if (event["kind"], event.get("step"), event.get("state")) == (
                    "job", tail_chain.TAG, "running"
                ):
                    running = event
        time.sleep(0.02)
    go.touch()
    process.wait(timeout=300)
    reader.join(timeout=10)

    assert running is not None, "".join(lines)
    answered = json.loads(result.read_text())
    assert answered["waited"] is True
    assert answered["code"] == int(ExitCode.PENDING_HUMAN)
    events = _events("".join(line for line in lines if line.startswith("{")))
    assert events[-1] == {**events[-1], "kind": "end", "exit_code": answered["code"]}
    assert all(output.progress_problems(event) == [] for event in events)


@pytest.mark.parametrize("human", [False, True])
def test_a_reader_that_closes_standard_error_leaves_the_run_its_exit_and_its_saved_run(
    tmp_path, human
):
    """Human output too: its refusal and gate screen go to standard error."""
    process, result = _child(tmp_path, **({"CRATEKIT_PROGRESS_CHILD_HUMAN": "1"} if human else {}))
    process.stderr.close()
    process.wait(timeout=300)

    answered = json.loads(result.read_text())
    assert answered["code"] == int(ExitCode.PENDING_HUMAN)
    assert answered["saved"] is True


@pytest.mark.parametrize("events, job_id", [(False, "j"), (True, None)])
def test_no_job_is_watched_without_events_or_without_a_job(monkeypatch, events, job_id):
    """Asserted on the watch's construction, not on its output, so a dead thread cannot pass."""
    built: list[tuple] = []
    monkeypatch.setattr(progress, "_Watch", lambda *args: built.append(args))
    writer = progress.Writer(io.StringIO(), verb="v", events=events)

    with progress.watching(writer, "tag", job_id):
        pass
    with progress.watching(lambda _line: None, "tag", "j"):
        pass

    assert built == []


def test_a_watched_job_is_reported_on_each_change_and_once_after_the_drive(machine, monkeypatch):
    from tests.test_sync_land import _enqueue

    cfg, _script = machine
    job = _enqueue(cfg, "tag.folder", {"folder": "/staged"}, "a.flac", "b.flac")
    stream = io.StringIO()
    writer = progress.Writer(stream, verb="sync.land", events=True)
    monkeypatch.setattr(progress, "WATCH_SECONDS", 3600.0)

    with progress.watching(writer, "tag", job.job_id):
        with jobs.open_store() as store:
            jobs.drive(store, job.job_id, lambda _job, _item: None)

    first, last = (json.loads(line) for line in stream.getvalue().splitlines())
    assert (first["state"], first["progress"]["settled"]) == ("queued", 0)
    assert (last["state"], last["progress"]["settled"], last["step"]) == ("succeeded", 2, "tag")

    # A watch over a drive that changed nothing reads the job as it starts and
    # writes it once more after, unchanged, since the last event of a drive
    # is always its job as the queue holds it then.
    with progress.watching(writer, "tag", job.job_id):
        pass
    again = [json.loads(line) for line in stream.getvalue().splitlines()][2:]
    assert [(event["state"], event["progress"]["settled"]) for event in again] == [
        ("succeeded", 2), ("succeeded", 2)
    ]


def test_a_writer_over_a_closed_standard_error_writes_nothing_anywhere(capsys):
    """A process started with fd 2 closed has None there, which print reads as stdout."""
    writer = progress.Writer(None, verb="v", events=True)
    writer("dropped")
    writer.end(run_id="r", exit_code=0)
    cli._to_stderr("a person's copy", None)

    assert capsys.readouterr().out == ""
