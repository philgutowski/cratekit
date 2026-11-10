"""U241: the core count is read in one place, and used as a ceiling and nothing else.

``cratekit.core.pool`` reads no core count, because sizing a pool from the
cores is the kill it exists to prevent. U241 lets a caller whose workers are
cheap pass a ceiling derived from the cores, which can only lower a plan.
Three things keep that from becoming the old defect under a new name, and each
is asserted here rather than intended:

1. the count is read by ``cratekit.core.cores`` and by no other shipped module,
   in any of the four spellings, as a name or as a string handed to ``getattr``;
2. what that module answers reaches the planner as its ``ceiling`` argument and
   reaches nothing else, checked on the syntax tree of every shipped module;
3. the planner still decides underneath it: memory and both pressure gates
   overrule any core count, which ``tests/test_analysis_ahead.py`` drives
   through the verb and the last test here drives on the planner itself.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path

import pytest

from cratekit.core import cores, pool
from tests.test_pool_sizing import CORE_COUNT_SPELLINGS, PACKAGE_ROOT, REPO_ROOT

GIB = 1024**3
CORES_PATH = PACKAGE_ROOT / "core" / "cores.py"


def shipped_modules() -> list[Path]:
    return [
        path
        for root in (PACKAGE_ROOT, REPO_ROOT / "scripts")
        for path in sorted(root.rglob("*.py"))
        if "_vendor" not in path.parts
    ]


# ---------------------------------------------------------------------------
# The reading
# ---------------------------------------------------------------------------


def test_the_allowance_of_this_process_is_preferred_to_the_machines_count(monkeypatch):
    monkeypatch.setattr(os, "sched_getaffinity", lambda pid: {0, 1, 2}, raising=False)
    monkeypatch.setattr(os, "cpu_count", lambda: 64)
    monkeypatch.setattr(os, "process_cpu_count", lambda: 64, raising=False)
    assert cores.usable_cores() == 3


@pytest.mark.parametrize("refusal", [OSError("no affinity here"), None], ids=["refused", "empty"])
def test_an_allowance_that_cannot_be_read_falls_through_to_the_machines_count(monkeypatch, refusal):
    def affinity(pid):
        if refusal is not None:
            raise refusal
        return set()

    monkeypatch.setattr(os, "sched_getaffinity", affinity, raising=False)
    monkeypatch.setattr(os, "process_cpu_count", lambda: 11, raising=False)
    monkeypatch.setattr(os, "cpu_count", lambda: 12)
    assert cores.usable_cores() == 11


def test_a_platform_with_no_allowance_reads_the_machines_count(monkeypatch):
    monkeypatch.delattr(os, "sched_getaffinity", raising=False)
    monkeypatch.delattr(os, "process_cpu_count", raising=False)
    monkeypatch.setattr(os, "cpu_count", lambda: 8)
    assert cores.usable_cores() == 8


@pytest.mark.parametrize("answer", [None, 0, -4, True, "8"])
def test_a_count_that_is_not_a_count_is_unknown(monkeypatch, answer):
    monkeypatch.delattr(os, "sched_getaffinity", raising=False)
    monkeypatch.delattr(os, "process_cpu_count", raising=False)
    monkeypatch.setattr(os, "cpu_count", lambda: answer)
    assert cores.usable_cores() is None


# ---------------------------------------------------------------------------
# The ceiling
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "count,reserved,expected",
    [(11, 2, 9), (4, 2, 2), (3, 2, 1), (2, 2, 1), (1, 2, 1), (8, 0, 8), (8, 1, 7)],
)
def test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one(
    count, reserved, expected
):
    assert cores.worker_ceiling(reserved=reserved, read=lambda: count) == expected


@pytest.mark.parametrize("answer", [None, 0, -1, True, 2.0, "4"])
def test_not_knowing_the_cores_is_a_ceiling_of_one(answer):
    assert cores.worker_ceiling(reserved=0, read=lambda: answer) == 1


def test_a_reading_that_raises_is_a_ceiling_of_one():
    def refuses():
        raise RuntimeError("this platform will not say")

    assert cores.worker_ceiling(reserved=0, read=refuses) == 1


@pytest.mark.parametrize("reserved", [-1, True, 1.5, "2"])
def test_what_is_kept_back_must_be_a_whole_count(reserved):
    with pytest.raises(ValueError, match="reserved"):
        cores.worker_ceiling(reserved=reserved, read=lambda: 8)


def test_the_reader_is_looked_up_when_called_so_a_test_can_stand_in(monkeypatch):
    monkeypatch.setattr(cores, "usable_cores", lambda: 10)
    assert cores.worker_ceiling(reserved=2) == 8


# ---------------------------------------------------------------------------
# The count is read here and nowhere else
# ---------------------------------------------------------------------------


def core_count_reads(source: str) -> list[str]:
    """Every way this source names a core count: as a name, or as a string for ``getattr``."""
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Attribute) and node.attr in CORE_COUNT_SPELLINGS:
            found.append(f"line {node.lineno}: .{node.attr}")
        elif isinstance(node, ast.Name) and node.id in CORE_COUNT_SPELLINGS:
            found.append(f"line {node.lineno}: {node.id}")
        elif isinstance(node, ast.alias) and node.name.split(".")[-1] in CORE_COUNT_SPELLINGS:
            found.append(f"line {node.lineno}: import {node.name}")
        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value in CORE_COUNT_SPELLINGS
        ):
            found.append(f"line {node.lineno}: the string {node.value!r}")
    return found


@pytest.mark.parametrize(
    "source",
    [
        "import os\nwidth = os.cpu_count() - 2\n",
        "import os\nwidth = len(os.sched_getaffinity(0))\n",
        "from os import process_cpu_count\n",
        "import os\nwidth = getattr(os, 'cpu_count')()\n",
        "import psutil\nwidth = len(psutil.Process().cpu_affinity())\n",
    ],
    ids=["cpu-count", "affinity", "imported", "through-getattr", "psutil"],
)
def test_the_walk_sees_a_core_count_read_in_every_spelling(source):
    assert core_count_reads(source) != []


def test_the_walk_is_silent_on_prose_and_on_the_one_reader_being_called():
    source = (
        '"""The source system sized its pool as cpu_count() less two."""\n'
        "from cratekit.core import cores, pool\n"
        "def plan(cost, items):\n"
        "    return pool.plan_pool(worker_bytes=cost, items=items,\n"
        "                          ceiling=cores.worker_ceiling(reserved=2))\n"
    )
    assert core_count_reads(source) == []


def test_no_shipped_module_but_the_one_reader_reads_a_core_count():
    offenders = {
        str(path.relative_to(REPO_ROOT)): reads
        for path in shipped_modules()
        if path != CORES_PATH and (reads := core_count_reads(path.read_text()))
    }
    assert not offenders, (
        f"a core count is read outside cratekit.core.cores: {offenders}. The count "
        f"is a ceiling handed to the planner and is read in one place."
    )
    assert core_count_reads(CORES_PATH.read_text()), "the one reader reads no core count"


# ---------------------------------------------------------------------------
# What the reader answers reaches the planner's ceiling and nothing else
# ---------------------------------------------------------------------------


def _parents(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    return {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}


def _called(node: ast.AST) -> str | None:
    """The last name of what a call calls: ``pool.plan_pool(...)`` is ``plan_pool``."""
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return None


def ceilings_used_as_anything_else(source: str) -> list[str]:
    """Every ``worker_ceiling`` or ``usable_cores`` use that is not the planner's ceiling.

    The one accepted shape is the call written directly as the ``ceiling``
    keyword of a ``plan_pool`` call. A count bound to a name first could then
    be multiplied, compared or handed to a pool as its width, which is the
    source system's defect, so that is refused too rather than traced.
    """
    tree = ast.parse(source)
    parents = _parents(tree)
    found: list[str] = []
    for node in ast.walk(tree):
        named = None
        if isinstance(node, ast.Attribute) and node.attr in ("worker_ceiling", "usable_cores"):
            named = node.attr
        elif isinstance(node, ast.Name) and node.id in ("worker_ceiling", "usable_cores"):
            named = node.id
        if named is None:
            continue
        call = parents.get(node)
        keyword = parents.get(call) if call is not None else None
        planner = parents.get(keyword) if keyword is not None else None
        accepted = (
            named == "worker_ceiling"
            and isinstance(call, ast.Call)
            and call.func is node
            and isinstance(keyword, ast.keyword)
            and keyword.arg == "ceiling"
            and _called(planner) == "plan_pool"
        )
        if not accepted:
            found.append(f"line {node.lineno}: {named}")
    return found


@pytest.mark.parametrize(
    "source",
    [
        "from cratekit.core import cores, pool\n"
        "def run(items):\n"
        "    width = cores.worker_ceiling(reserved=2)\n"
        "    return pool.plan_pool(worker_bytes=1, items=items, ceiling=width)\n",
        "from cratekit.core import cores\n"
        "def run(items):\n"
        "    return min(items, cores.usable_cores() - 2)\n",
        "from cratekit.core import cores, pool\n"
        "def run(items):\n"
        "    return pool.plan_pool(worker_bytes=1, items=cores.worker_ceiling(reserved=0))\n",
        "from cratekit.core.cores import worker_ceiling\n"
        "from concurrent.futures import ThreadPoolExecutor\n"
        "def run():\n"
        "    return ThreadPoolExecutor(max_workers=worker_ceiling(reserved=1))\n",
    ],
    ids=["bound-to-a-name", "the-raw-count", "as-the-item-count", "as-a-pools-width"],
)
def test_a_ceiling_used_as_anything_but_the_planners_ceiling_is_seen(source):
    assert ceilings_used_as_anything_else(source) != []


def test_the_accepted_shape_is_silent():
    source = (
        "from cratekit.core import cores, pool\n"
        "def plan(cost, items):\n"
        "    return pool.plan_pool(worker_bytes=cost, items=items,\n"
        "                          ceiling=cores.worker_ceiling(reserved=2))\n"
    )
    assert ceilings_used_as_anything_else(source) == []


def test_every_shipped_use_of_the_core_ceiling_is_the_planners_ceiling():
    offenders = {
        str(path.relative_to(REPO_ROOT)): uses
        for path in shipped_modules()
        if path != CORES_PATH and (uses := ceilings_used_as_anything_else(path.read_text()))
    }
    assert not offenders, (
        f"the core ceiling is used as something other than plan_pool's ceiling: "
        f"{offenders}"
    )
    light = (PACKAGE_ROOT / "analysis" / "light.py").read_text()
    assert "worker_ceiling" in light, "the light pass no longer takes its ceiling from the cores"


# ---------------------------------------------------------------------------
# And the planner still decides underneath it
# ---------------------------------------------------------------------------


def _calm() -> pool.Pressure:
    return pool.Pressure(swap_used_bytes=0, used_percent=10.0)


def test_a_ceiling_from_many_cores_never_widens_what_memory_affords():
    ceiling = cores.worker_ceiling(reserved=2, read=lambda: 64)
    assert ceiling == 62
    afforded = pool.plan_pool(
        worker_bytes=GIB,
        items=500,
        ceiling=ceiling,
        headroom_percent=50,
        read_available=lambda: 8 * GIB,
        read_pressure=_calm,
    )
    # (8 less the 2 reserved) at half is 3 gibibytes: three workers, not sixty two.
    assert afforded.workers == 3 and afforded.bound is pool.Bound.AVAILABLE_MEMORY
    refused = pool.plan_pool(
        worker_bytes=GIB,
        items=500,
        ceiling=ceiling,
        read_available=lambda: 512 * GIB,
        read_pressure=lambda: pool.Pressure(swap_used_bytes=2 * GIB, used_percent=10.0),
    )
    assert refused.workers == 1 and refused.bound is pool.Bound.MEMORY_PRESSURE
    unread = pool.plan_pool(
        worker_bytes=GIB, items=500, ceiling=ceiling, read_available=lambda: -1
    )
    assert unread.workers == 1 and unread.bound is pool.Bound.MEMORY_UNREADABLE
