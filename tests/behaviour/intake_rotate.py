"""Intake's rotation scenarios: stale INBOX batches moved into Old and expired ones removed (U307).

`crate inbox rotate --as-of` over three batches in INBOX and one in Old, a
person's playlist and folder beside them: the plan as a person reads it,
the gate as the envelope, the answer, and the rotation that moves the forty
and hundred day batches into Old and removes the one past expiry, with no
track going anywhere. Run again, the batch moved past expiry goes, and then
nothing does. An INBOX that gained a batch after the answer is refused
stale with nothing written, and a machine with no backup acknowledgment
refuses before the gate. On the rotation suite's own library.

A file of its own, because the rotation suite builds its own ``machine``
with eight tracks filed, as the native landing suite builds another.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_inbox_rotate import GATE, VERB, _cut_over_intake, _node
from tests.test_inbox_rotate import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_inbox_rotate import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_inbox_rotate import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_inbox_rotate import four_batches as four_batches  # noqa: PLC0414
from tests.test_inbox_rotate import machine as machine  # noqa: PLC0414
from tests.test_inbox_rotate import native_library as native_library  # noqa: PLC0414

OK = int(ExitCode.OK)
ASKED = int(ExitCode.DECISION_REQUIRED)


def _two_acts(stage):
    """The plan as a person reads it and as the envelope, its answer, and the acting drive."""
    assert stage.crate(*VERB).code == ASKED
    refused = stage.json(*VERB)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "approve").code == OK
    return stage.json("--run", run_id, *VERB)


def test_stale_batches_move_into_old_and_the_expired_go(stage, four_batches):
    first = _two_acts(stage)
    assert first.code == OK, first.stdout
    totals = first.envelope["data"]["totals"]
    assert (totals["moved"], totals["removed"]) == (2, 1)

    second = _two_acts(stage)
    assert second.code == OK, second.stdout
    third = _two_acts(stage)
    assert third.code == OK, third.stdout
    assert third.envelope["outcome"] == "no_op"


def test_an_inbox_changed_after_the_answer_is_stale_and_writes_nothing(stage, native_library):
    cfg, root_id = native_library
    _node(cfg, "2026-08-20 Set", under=root_id, age=44, tracks=("t1",), batch_folder=True)
    refused = stage.json(*VERB)
    assert refused.code == ASKED, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, GATE, "approve").code == OK
    _node(cfg, "2026-08-19 Set", under=root_id, age=45, tracks=("t2",), batch_folder=True)

    stale = stage.json("--run", run_id, *VERB)
    assert stale.code == int(ExitCode.DECISION_STALE), stale.stdout


def test_no_acknowledgment_refuses_before_the_gate(stage, machine):
    _cut_over_intake(machine)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.ACK_REQUIRED), refused.stdout
    assert stage.crate(*VERB).code == refused.code
