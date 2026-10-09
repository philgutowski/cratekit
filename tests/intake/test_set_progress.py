"""R-924: intake set says which phase it is in, and how far, while it runs.

A five hour mix was 557 MB of download and 732 paid calls with nothing on the
screen. These drive the real dispatcher with the fake fetcher and the fake
carver and transport the U104 and worker tests already use, and read what a
person would see on standard error.
"""

from __future__ import annotations

import io
import json
import threading
import time
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import acrcloud, fetch
from tests.cli_drive import drive
from tests.intake import test_workers as workers
from tests.intake.test_recognition import FakeCarver, miss
from tests.intake.test_set_fetch import URL, FakeFetcher, nothing_left
from tests.intake.test_workers import recording, three_tracks

cfg = workers.cfg
library = workers.library
recognised = workers.recognised


@pytest.fixture
def fetcher(monkeypatch) -> FakeFetcher:
    fake = FakeFetcher()
    monkeypatch.setattr(fetch, "fetcher", lambda: fake)
    return fake


def human(argv: list[str]) -> tuple[int, str, list[str]]:
    """One invocation in human output: the code, standard output, standard error's lines."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue().splitlines()


def counter_lines(lines: list[str]) -> list[str]:
    return [one for one in lines if one.startswith("identifying: sent ")]


def test_human_output_says_the_fetch_then_the_plan_then_the_count(
    cfg, library, recognised, fetcher
):
    three_tracks(recognised)
    code, out, err = human(["intake", "set", URL])
    assert code == int(ExitCode.OK), err
    assert err[0] == f"fetching: {URL}"
    # The fake lands seventeen bytes, which is 0.0 MB. The seconds are the
    # machine's, so only their shape is asserted.
    assert err[1].startswith("fetched: 0.0 MB in ") and err[1].endswith("s")
    assert err[2] == (
        "identifying: 3 chunk(s) planned, 0 answered from the recognition cache, "
        "3 paid call(s) to send"
    )
    assert counter_lines(err) == [
        "identifying: sent 1 of 3 call(s)",
        "identifying: sent 3 of 3 call(s)",
    ]
    assert len(err) == 5
    # The progress is not the result: none of it is on standard output.
    assert "fetching" not in out and "identifying" not in out
    assert nothing_left()


def test_json_output_carries_no_progress_and_stays_one_document(
    cfg, library, recognised, fetcher
):
    three_tracks(recognised)
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", "intake", "set", URL], stdout=out, stderr=err)
    assert code == int(ExitCode.OK), err.getvalue()
    document = json.loads(out.getvalue())
    assert document["data"]["progress"]["calls"] == 3
    assert "fetching" not in out.getvalue() and "identifying" not in out.getvalue()
    # Human output only: a successful JSON run writes nothing to standard error.
    assert err.getvalue() == ""
    assert len(recognised.requests) == 3


def test_the_planned_count_is_the_chunks_the_carver_is_asked_for(
    cfg, library, recognised, monkeypatch
):
    carver = FakeCarver(600.0)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: carver)
    planned = acrcloud.planned_calls(600.0)
    recognised.answers[:] = [miss() for _ in range(planned)]
    code, _out, err = human(["intake", "set", str(recording(library))])
    assert code == int(ExitCode.OK), err
    plan = [one for one in err if "planned" in one]
    assert len(plan) == 1
    said = int(plan[0].split("identifying: ")[1].split(" chunk")[0])
    assert said == len(carver.carved) == len(recognised.requests) == planned == 24
    # The first call, every twentieth, and the last.
    assert counter_lines(err) == [
        f"identifying: sent {n} of {planned} call(s)" for n in (1, acrcloud.PROGRESS_EVERY, planned)
    ]
    # A local recording fetches nothing and says nothing about fetching.
    assert not [one for one in err if one.startswith("fetch")]


def test_a_cached_recording_says_so_and_counts_no_calls(cfg, library, recognised):
    three_tracks(recognised)
    path = recording(library)
    code, _envelope = drive(["intake", "identify", str(path)])
    assert code == int(ExitCode.OK)
    assert len(recognised.requests) == 3

    code, _out, err = human(["intake", "set", str(path)])
    assert code == int(ExitCode.OK), err
    assert err == [
        "identifying: all 3 chunk(s) are answered from the recognition cache, "
        "so no call is sent"
    ]
    assert len(recognised.requests) == 3


def test_a_parted_set_says_its_parts_in_the_plan(cfg, library, recognised, monkeypatch):
    carver = FakeCarver(600.0)
    monkeypatch.setattr(acrcloud, "FfmpegCarver", lambda: carver)
    monkeypatch.setattr(acrcloud.Budget, "from_config", classmethod(
        lambda cls, recognition: cls(per_run=10, monthly=None)
    ))
    recognised.answers[:] = [miss() for _ in range(24)]
    code, _out, err = human(["intake", "set", str(recording(library))])
    assert code == int(ExitCode.OK), err
    assert [one for one in err if "planned" in one] == [
        "identifying: 24 chunk(s) planned, 0 answered from the recognition cache, "
        "24 paid call(s) to send in 3 parts"
    ]


class SlowFetcher:
    """Writes a partial, then waits until the watcher has reported it."""

    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def fetch(self, url: str, directory: Path) -> Path:
        (directory / "fetched.mp3.part").write_bytes(b"\0" * 2_000_000)
        deadline = time.monotonic() + 10
        while not any("so far" in one for one in self.lines):
            if time.monotonic() > deadline:
                raise AssertionError("the watcher never reported the partial")
            time.sleep(0.005)
        (directory / "fetched.mp3.part").rename(directory / "fetched.mp3")
        return directory / "fetched.mp3"


def test_the_watcher_reports_the_bytes_written_while_the_download_runs(
    cfg, library, monkeypatch
):
    monkeypatch.setattr(fetch, "FETCH_PROGRESS_SECONDS", 0.01)
    lines: list[str] = []
    with fetch.fetched(URL, library, SlowFetcher(lines), progress=lines.append) as got:
        assert got.path.name == "fetched.mp3"
    assert lines[0] == f"fetching: {URL}"
    assert any(one.startswith("fetching: 2.0 MB so far, ") for one in lines)
    assert lines[-1].startswith("fetched: 2.0 MB in ")
    # Stopped and joined before the block was lent: nothing outlives the fetch.
    assert not [one for one in threading.enumerate() if one.name == "mix-fetch-progress"]


def test_a_fetch_that_raises_still_stops_the_watcher(cfg, library, monkeypatch):
    monkeypatch.setattr(fetch, "FETCH_PROGRESS_SECONDS", 0.01)
    lines: list[str] = []
    with pytest.raises(fetch.SetFetchFailed):
        with fetch.fetched(URL, library, FakeFetcher(fail="404"), progress=lines.append):
            pass
    assert lines == [f"fetching: {URL}"]
    assert not [one for one in threading.enumerate() if one.name == "mix-fetch-progress"]
