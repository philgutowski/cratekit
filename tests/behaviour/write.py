"""The write layer's scenarios: a guarded tree write and an XML splice (U297).

On the routing suite's library; the tree write goes through the session, so the
capture holds its snapshot, session record and job files too.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_routing_workers import _write_export
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414
from tests.test_routing_workers import native as native  # noqa: PLC0414
from tests.test_routing_workers import stocked as stocked  # noqa: PLC0414
from tests.test_routing_workers import tagged as tagged  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_guarded_tree_write(stage, acknowledged, native):
    """`crate rebuild`, queued and then run: the governed tree takes its track."""
    queued = stage.json("rebuild", "--actor", "a-person")
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    done = stage.crate("rebuild", "--actor", "a-person", "--job", job_id)
    assert done.code == OK, done.stderr
    # The finished job as JSON and the report over the library, as the verbs
    # read back what was written.
    assert stage.json("rebuild", "--actor", "a-person", "--job", job_id).code == OK
    stage.crate("route", "unplaced")


def test_xml_splice(stage, configured, tagged, tmp_path):
    """`crate route inbox --export`, applied: three tracks spliced into their subs."""
    export = _write_export(configured, tmp_path / "exports")
    shown = stage.crate("route", "inbox", "--export", str(export))
    assert not export.with_name("library_FRESH_routed.xml").exists(), shown.stdout
    applied = stage.json("-d", "route.inbox.apply=apply", "route", "inbox", "--export", str(export))
    assert applied.code == OK, applied.stdout
    assert applied.envelope["data"]["totals"]["inserted"] == 3
    assert export.with_name("library_FRESH_routed.xml").is_file()
