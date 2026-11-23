"""Label sync's go: one summary, one gate, one download by the fake adapter (U308).

`crate label sync --go` shows one summary at its gate, downloads what the saved
answers took through `acquire download`'s worker, and stops at the landing's
gate; a declined go downloads nothing.
"""

from __future__ import annotations

import os

from cratekit.core.exit_codes import ExitCode
from tests import behaviour
from tests.acquire_fakes import FakeSource
from tests.test_label_sync import bind
from tests.test_label_sync_go import GATE, land_every
from tests.test_label_sync_go import installed as installed  # noqa: PLC0414
from tests.test_label_sync_go import no_vocal_model as no_vocal_model  # noqa: PLC0414
from tests.test_label_sync_go import script as script  # noqa: PLC0414
from tests.test_label_sync_go import tail as tail  # noqa: PLC0414

OK = int(ExitCode.OK)
SYNC = ("label", "sync")
GO = (*SYNC, "--go")


def _landed_at_the_instant(monkeypatch) -> None:
    """The fake adapter's files given the pinned instant as they land, since the go
    records each by its time before the stage can settle it."""
    real = FakeSource.fetch
    stamp = behaviour.INSTANT.timestamp()

    def fetch(self, request, destination):
        path = real(self, request, destination)
        os.utime(path, (stamp, stamp))
        return path

    monkeypatch.setattr(FakeSource, "fetch", fetch)


def test_answers_summarised_gated_and_downloaded(stage, installed, monkeypatch, script):
    for name in ("Alpha Works", "Beta Works", "Delta Works"):
        assert stage.crate("label", "registry", "add", name).code == OK
    bind(
        monkeypatch,
        {
            "alpha-works": [("a2", "2026", 2), ("a1", "2025", 1)],
            "beta-works": [("b1", "2026", 3)],
            "delta-works": [("d1", "2026", 1)],
        },
    )
    for label_id, *answer in (
        ("alpha-works", "all"),
        ("beta-works", "pick", "--release", "b1"),
        ("delta-works", "not-now"),
    ):
        assert stage.crate(*SYNC, "--next").code == OK
        assert stage.crate(*SYNC, "--answer", *answer[:1], "--label", label_id, *answer[1:]).code == OK
    land_every(script, ("a2", 2), ("a1", 1), ("b1", 3))
    _landed_at_the_instant(monkeypatch)

    # Declined first: the summary at the gate, and nothing downloaded.
    declined = stage.json(*GO)
    assert declined.code == int(ExitCode.DECISION_REQUIRED), declined.stdout
    assert stage.decide(declined.envelope["run_id"], GATE, "abort").code == OK
    assert stage.crate("--run", declined.envelope["run_id"], *GO).code == OK

    assert stage.crate(*GO).code == int(ExitCode.DECISION_REQUIRED)
    asked = stage.json(*GO)
    run_id = asked.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK
    done = stage.crate("--run", run_id, *GO)
    assert done.code == int(ExitCode.PENDING_HUMAN), done.stderr
    # A second go refuses while the staging folder holds the download.
    assert stage.crate(*GO).code == int(ExitCode.REFUSED_BY_POLICY)
