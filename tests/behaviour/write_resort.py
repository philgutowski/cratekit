"""The write layer's resort scenarios: the routing tree resorted behind its gate (U302).

`crate route resort` plans the memberships every routing tree lacks, stops at
its explicit gate showing each add and the trees it leaves alone, and once the
gate is answered queues a job whose worker, ``route resort --job``, writes the
approved adds inside one guarded database session. On the resort suite's own
library: a disposable database where the genre tree and the intake tree have
both cut over, the intake tree holding one landed batch, and two files read as
the genre sub at one energy. Its refusal is the pin on the file a plan read: an
approval recorded over a copy of the database does not approve the live file,
though both plan the same adds under the same digest.

A file of its own beside ``write.py``, because the resort suite and the
routing suite that file borrows from each call their set up machine
``configured`` and their readings ``tagged``.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests.test_resort_scope import GATE
from tests.test_resort_scope import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_resort_scope import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_resort_scope import both_native as both_native  # noqa: PLC0414
from tests.test_resort_scope import configured as configured  # noqa: PLC0414
from tests.test_resort_scope import library as library  # noqa: PLC0414
from tests.test_resort_scope import tagged as tagged  # noqa: PLC0414

OK = int(ExitCode.OK)
VERB = ("route", "resort")


def test_a_resort_planned_queued_and_run_by_its_worker(stage, both_native):
    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    assert refused.envelope["cause"]["detail"]["shown"]["adds"] == 4
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    queued = stage.json("--run", run_id, *VERB)
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    assert job_id
    done = stage.json("--run", run_id, *VERB, "--job", job_id)
    assert done.code == OK, done.stdout
    # Ask again: the tree holds every add, so the gate offers none.
    stage.crate(*VERB)


def test_an_answer_over_a_copy_does_not_approve_the_live_file(stage, both_native):
    cfg = config.load()
    live = Path(cfg.library.db_path)
    copy = live.with_name("rehearsal.db")
    copy.write_bytes(live.read_bytes())
    config.save(dataclasses.replace(cfg, library=dataclasses.replace(cfg.library, db_path=copy)))
    config.reset_cache()
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "apply").code == OK

    config.save(cfg)
    config.reset_cache()
    stale = stage.json("--run", run_id, *VERB)
    assert stale.code != OK, stale.stdout
    assert stale.envelope["cause"]["reason"] == "decision-stale"
