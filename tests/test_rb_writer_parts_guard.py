"""The guarded writer's source scans, read over the writer AND its parts (R-1890).

``tests/test_rb_writer_guard.py`` reads none of the parts U300 split out and is never
edited, so its checks run here over every part (``tests/_split_modules.py``), refusals
read through both factory spellings. The fix in ``tests/_source_guards.py`` is proved here.
"""

from __future__ import annotations

import ast

from cratekit.core.cause import REASONS
from cratekit.core.exit_codes import ExitCode, meaning_of
from tests import _source_guards as guard
from tests._split_modules import files_of

WRITER = "cratekit.core.rb_writer"

#: The writer's two refusal constructors; ``_running`` always raises ``rekordbox-running``.
REFUSAL_FACTORIES = frozenset({"_unavailable", "_running"})


def _called_name(node: ast.Call) -> str | None:
    """The name a call is made by: ``f(...)``, ``x.f(...)`` and ``_writer().f(...)``."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _refusal_calls(source: str) -> list[ast.Call]:
    """Every call of a refusal constructor in ``source``, by any spelling."""
    return [
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call) and _called_name(node) in REFUSAL_FACTORIES
    ]


def raised_reasons(source: str) -> set[str]:
    """Every reason slug ``source`` raises, read off its syntax tree (P3)."""
    reasons: set[str] = set()
    for node in _refusal_calls(source):
        if _called_name(node) == "_running":
            reasons.add("rekordbox-running")
        elif node.args and isinstance(node.args[0], ast.Constant):
            reasons.add(node.args[0].value)
    return reasons


def _parts() -> list[tuple[str, str]]:
    return [(path.name, path.read_text(encoding="utf-8")) for path in files_of(WRITER)[1:]]


# ── the scope: what this file reads ──────────────────────────────────────────


def test_the_scans_read_every_part_the_writer_was_split_into():
    """A scan that reads nothing passes everything, so its scope is pinned first."""
    names = {path.name for path in files_of(WRITER)}
    for part in ("rb_tables.py", "rb_probes.py", "rb_copies.py", "rb_nodes.py",
                 "rb_changes.py", "rb_removal.py"):
        assert part in names, f"the writer's scan does not read {part}"
    assert files_of(WRITER)[0].name == "rb_writer.py"


def test_the_parts_raise_refusals_through_the_accessor_and_the_scan_sees_them():
    """Without the accessor spelling the parts' refusals read as none at all."""
    seen = {name: raised_reasons(source) for name, source in _parts()}
    assert seen["rb_removal.py"], "the scan reads no refusal in rb_removal, so it is not reading it"
    assert "rekordbox-running" in seen["rb_probes.py"]


# ── never a bare exception ───────────────────────────────────────────────────


def test_no_part_of_the_writer_raises_a_bare_runtime_error_or_system_exit():
    """KTD25 over the writer and every part: never a literal status or an untyped error."""
    for path in files_of(WRITER):
        source = path.read_text(encoding="utf-8")
        assert "RuntimeError(" not in source, f"{path.name} raises a bare RuntimeError"
        assert "SystemExit" not in source, f"{path.name} names SystemExit"


# ── every refusal is in the reserved vocabulary ──────────────────────────────


def test_every_refusal_the_writer_or_a_part_raises_through_a_factory_is_reserved():
    for path in files_of(WRITER):
        for reason in sorted(raised_reasons(path.read_text(encoding="utf-8"))):
            assert reason in REASONS, f"{path.name} raises {reason!r}, not a declared reason"
            assert REASONS[reason] is not ExitCode.OK, (path.name, reason)
            assert meaning_of(REASONS[reason]).remedy is not None, (path.name, reason)


def test_every_refusal_names_its_reason_as_a_literal_the_scan_can_read():
    """Every ``_unavailable`` call names its reason literally, or both checks above miss it."""
    unread = [
        f"{path.name}:{node.lineno}"
        for path in files_of(WRITER)
        for node in _refusal_calls(path.read_text(encoding="utf-8"))
        if _called_name(node) == "_unavailable"
        and not (node.args and isinstance(node.args[0], ast.Constant))
    ]
    assert not unread, f"a refusal whose reason the scan cannot read: {unread}"


def test_the_reason_scan_reads_both_spellings_and_skips_what_is_not_a_refusal():
    source = (
        "def a():\n    raise _unavailable('db-schema-pin-drift', 'm')\n"
        "def b():\n    raise _writer()._unavailable('app-version-pin-drift', 'm')\n"
        "def c():\n    raise rb_writer._running('m')\n"
        "def d():\n    unavailable('not-a-refusal', 'm')\n"
    )
    assert raised_reasons(source) == {
        "db-schema-pin-drift", "app-version-pin-drift", "rekordbox-running",
    }


# ── the soft-delete marker, read through the parts' accessor ─────────────────

_ACCESSOR = (
    "def _writer():\n"
    "    from cratekit.core import rb_writer\n"
    "\n"
    "    return rb_writer\n"
    "\n"
    "\n"
)
#: A permissive read of the column through the accessor.
READS = "def read(row):\n    return getattr(row, _writer().SOFT_DELETE_COLUMN, 0)\n"


def test_the_soft_delete_guard_fires_on_a_permissive_read_through_the_accessor():
    """``_writer().SOFT_DELETE_COLUMN``, the parts' spelling, names the column (R-1890)."""
    evasions = (
        "def read(row):\n    return getattr(row, _writer().SOFT_DELETE_COLUMN, 0)\n",
        "def read(row):\n    return row.get(_writer().SOFT_DELETE_COLUMN, False)\n",
        "def read(row, w=None):\n    return getattr(row, _writer(w).SOFT_DELETE_COLUMN, 0)\n",
        "COLUMN = _writer().SOFT_DELETE_COLUMN\n"
        "def read(row):\n    return getattr(row, COLUMN, None)\n",
        "def read(row):\n    w = _writer()\n    return getattr(row, w.SOFT_DELETE_COLUMN, 0)\n",
    )
    for evasion in evasions:
        source = _ACCESSOR + evasion
        assert guard.permissive_soft_delete_reads(source), evasion
        assert guard.reads_soft_delete_marker(source), evasion


def test_the_accessor_is_recognized_by_the_import_shapes_the_guard_knows_and_nothing_else():
    """The shapes ``_writer_imports`` names; its known limits list what it does not."""
    for accessor in (
        _ACCESSOR,
        "def _writer():\n    import cratekit.core.rb_writer as w\n    return w\n",
        "def _writer():\n    import cratekit.core.rb_writer\n    return cratekit.core.rb_writer\n",
        "def _writer():\n    from cratekit.core import rb_writer as w\n    return w\n",
        "def _writer():\n    from . import rb_writer\n    return rb_writer\n",
        "if True:\n    def _writer():\n        from cratekit.core import rb_writer\n"
        "        return rb_writer\n",
    ):
        assert guard.permissive_soft_delete_reads(accessor + READS), accessor
    for not_one in (
        "def _writer():\n    from cratekit.core import config\n    return config\n",
        "def _writer():\n    from cratekit.core import rb_writer\n    return None\n",
        "",
    ):
        assert not guard.permissive_soft_delete_reads(not_one + READS), not_one


def test_the_soft_delete_guard_stays_quiet_on_the_parts_correct_reads():
    """Naming the column through the accessor is not a read; reading it strictly is fine."""
    for correct in (
        "def judge(columns):\n    return _writer().SOFT_DELETE_COLUMN in columns\n",
        "def read(row):\n    return getattr(row, _writer().SOFT_DELETE_COLUMN)\n",
        "def read(row):\n    return row[_writer().SOFT_DELETE_COLUMN]\n",
    ):
        assert not guard.permissive_soft_delete_reads(_ACCESSOR + correct), correct


# ── the accessor's one home (U329) ───────────────────────────────────────────


def test_the_accessor_imported_from_its_one_home_names_the_column():
    """``from cratekit.core.rb_call_time import writer as _writer``, the parts' spelling since U329."""
    for accessor in (
        "from cratekit.core.rb_call_time import writer as _writer\n",
        "from .rb_call_time import writer as _writer\n",
    ):
        assert guard.permissive_soft_delete_reads(accessor + READS), accessor
    bare = "from cratekit.core.rb_call_time import writer\n"
    assert guard.permissive_soft_delete_reads(bare + READS.replace("_writer()", "writer()"))
    for not_one in (
        "from cratekit.core.session_call_time import session as _writer\n",
        "from cratekit.core.other import writer as _writer\n",
    ):
        assert not guard.permissive_soft_delete_reads(not_one + READS), not_one


def test_every_accessor_read_of_the_column_in_the_parts_is_seen_by_the_guard():
    """Each ``_writer().SOFT_DELETE_COLUMN`` in a part names the column, so none is unread."""
    seen = 0
    for name, source in _parts():
        tree = ast.parse(source)
        names = guard.SoftDeleteNames(tree)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr == guard.SOFT_DELETE_CONSTANT
                and isinstance(node.value, ast.Call)
            ):
                assert names._is_column(node), f"{name}:{node.lineno} is not read as the column"
                seen += 1
    assert seen >= 4, f"only {seen} accessor reads of the column in the parts; the scan reads nothing"
