"""The guarded writer's source scans, read over the writer AND its parts (R-1890).

``tests/test_rb_writer_guard.py`` scans ``inspect.getsource(rb_writer)`` for two
things: that the writer raises no bare ``RuntimeError`` or ``SystemExit``, and,
through ``_raised_reasons``, that every refusal it raises has a reserved code
and a remedy and every reserved writer slug is raised. U300 moved code from
``rb_writer.py`` into parts (``rb_tables``, ``rb_probes``, ``rb_copies``,
``rb_nodes``, ``rb_changes``, ``rb_removal``), and ``getsource`` of the module
reads none of them, so a bare ``RuntimeError("...")`` or a refusal with no
reserved code written in a part passed both.

THAT FILE IS NOT EDITED HERE, AND THAT IS A RULE, NOT A PREFERENCE. It is one of
the two beat grid suites, which under the refactor epic are never edited,
trimmed, moved or renamed, and every name they import keeps its module. So the
same checks are applied here to the writer and its parts, read through
``tests/_split_modules.py``, and the scans in the beat grid suite stay as they
are beside them: a shape in ``rb_writer.py`` fails both files, a shape in a part
fails this one.

A part raises the writer's refusals through its call time accessor,
``_writer()._unavailable(...)`` and ``_writer()._running(...)``, which the beat
grid suite's scan, keyed on a bare ``_unavailable`` name, does not see. Both
spellings are read here, and any attribute spelling ending in the name
(``rb_writer._unavailable``, ``W._unavailable``) with them.

The third item R-1890 names in that file, the soft-delete guard's resolution of
``_writer().SOFT_DELETE_COLUMN``, is not a scan in the suite but a rule in
``tests/_source_guards.py``, fixed there and proved below; the suite's package
wide assertion reads the fixed rule without an edit.
"""

from __future__ import annotations

import ast

from tests import _source_guards as guard
from tests._split_modules import files_of, source_of

WRITER = "cratekit.core.rb_writer"

#: The writer's two refusal constructors, ``_unavailable(reason, message)`` and
#: ``_running(message)``, the second of which always raises ``rekordbox-running``.
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
    """The beat grid suite's KTD25 scan, over the writer and every part.

    Never a literal status, never an untyped error: a refusal that is a bare
    ``RuntimeError`` collapses to status one downstream and cannot be recovered.
    """
    for path in files_of(WRITER):
        source = path.read_text(encoding="utf-8")
        assert "RuntimeError(" not in source, f"{path.name} raises a bare RuntimeError"
        assert "SystemExit" not in source, f"{path.name} names SystemExit"


# ── every refusal is in the reserved vocabulary ──────────────────────────────


def test_every_refusal_the_writer_or_a_part_raises_has_a_reserved_code_and_a_remedy():
    from cratekit.core.cause import REASONS
    from cratekit.core.exit_codes import ExitCode, meaning_of

    for path in files_of(WRITER):
        for reason in sorted(raised_reasons(path.read_text(encoding="utf-8"))):
            assert reason in REASONS, f"{path.name} raises {reason!r}, not a declared reason"
            assert REASONS[reason] is not ExitCode.OK, (path.name, reason)
            assert meaning_of(REASONS[reason]).remedy is not None, (path.name, reason)


def test_every_refusal_names_its_reason_as_a_literal_the_scan_can_read():
    """A slug held in a variable is a refusal the two checks above cannot see.

    Read as absence, it would pass both: the code check reads no slug to test,
    and the vocabulary check is satisfied by the other call sites. So every
    ``_unavailable`` call in the writer and its parts names its reason literally.
    """
    unread = [
        f"{path.name}:{node.lineno}"
        for path in files_of(WRITER)
        for node in _refusal_calls(path.read_text(encoding="utf-8"))
        if _called_name(node) == "_unavailable"
        and not (node.args and isinstance(node.args[0], ast.Constant))
    ]
    assert not unread, f"a refusal whose reason the scan cannot read: {unread}"


def test_the_reserved_writer_vocabulary_is_raised_by_the_writer_or_a_part():
    from tests.test_cli_contract import WRITER_REFUSALS

    raised = raised_reasons(source_of(WRITER))
    unused = {slug for slug in WRITER_REFUSALS.values() if slug not in raised}
    assert not unused, f"reserved for the guarded writer but never raised: {sorted(unused)}"


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


def test_the_soft_delete_guard_fires_on_a_permissive_read_through_the_accessor():
    """The parts' spelling, ``_writer().SOFT_DELETE_COLUMN``, names the column.

    Before R-1890 the guard resolved ``rb_writer.SOFT_DELETE_COLUMN`` only by the
    module's local name, so a part reading the marker through its accessor
    with a falsey default read every soft-deleted row as active and passed.
    """
    evasions = (
        "def read(row):\n    return getattr(row, _writer().SOFT_DELETE_COLUMN, 0)\n",
        "def read(row):\n    return row.get(_writer().SOFT_DELETE_COLUMN, False)\n",
        "COLUMN = _writer().SOFT_DELETE_COLUMN\n"
        "def read(row):\n    return getattr(row, COLUMN, None)\n",
        "def read(row):\n    w = _writer()\n    return getattr(row, w.SOFT_DELETE_COLUMN, 0)\n",
    )
    for evasion in evasions:
        source = _ACCESSOR + evasion
        assert guard.permissive_soft_delete_reads(source), evasion
        assert guard.reads_soft_delete_marker(source), evasion


def test_the_accessor_is_recognized_by_every_import_shape_and_by_nothing_else():
    reads = "def read(row):\n    return getattr(row, _writer().SOFT_DELETE_COLUMN, 0)\n"
    for accessor in (
        _ACCESSOR,
        "def _writer():\n    import cratekit.core.rb_writer as w\n    return w\n",
        "def _writer():\n    from cratekit.core import rb_writer as w\n    return w\n",
        "def _writer():\n    from . import rb_writer\n    return rb_writer\n",
    ):
        assert guard.permissive_soft_delete_reads(accessor + reads), accessor
    for not_one in (
        "def _writer():\n    from cratekit.core import config\n    return config\n",
        "def _writer():\n    from cratekit.core import rb_writer\n    return None\n",
        "",
    ):
        assert not guard.permissive_soft_delete_reads(not_one + reads), not_one


def test_the_soft_delete_guard_stays_quiet_on_the_parts_correct_reads():
    """Naming the column through the accessor is not a read; reading it strictly is fine."""
    for correct in (
        "def judge(columns):\n    return _writer().SOFT_DELETE_COLUMN in columns\n",
        "def read(row):\n    return getattr(row, _writer().SOFT_DELETE_COLUMN)\n",
        "def read(row):\n    return row[_writer().SOFT_DELETE_COLUMN]\n",
    ):
        assert not guard.permissive_soft_delete_reads(_ACCESSOR + correct), correct
