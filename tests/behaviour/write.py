"""The write layer's scenarios: a guarded tree write and an XML splice (U297).

Both run on the routing suite's own library: its disposable database with an
adopted root and a cut over registry for the tree write, and its fresh export
for the splice. The tree write goes through the session, so it also captures
what a gated database session leaves behind: the snapshot, the session record
and the job's own files.
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
    # A second look at the finished job, as JSON, and the report over the
    # library it left, so the capture holds what was written as the verbs
    # themselves read it back.
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
