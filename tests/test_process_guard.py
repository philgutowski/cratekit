"""The rekordbox process guard has one name list and one matching rule.

Two guards that answer "is rekordbox running" once drifted on Windows' ``.exe``
suffix, invisible to each module's own tests, so this file puts them side by
side. Every set is derived by walking or introspecting, never hand listed.
"""

from __future__ import annotations

import ast
import functools
from pathlib import Path

import pytest

from cratekit.core import processes, rb_writer
from cratekit.modules.tools import backup

SRC = Path(__file__).resolve().parent.parent / "src" / "cratekit"


@functools.cache
def _scanned() -> tuple[list[str], list[tuple[str, int, object]]]:
    """One pass over every module: each assignment to ``REKORDBOX_PROCESSES``, and
    every constant a tuple, list, set or comparison encloses, with its place."""
    definers: list[str] = []
    enclosed: list[tuple[str, int, object]] = []
    containers = (ast.Tuple, ast.List, ast.Set, ast.Compare)
    for path in SRC.rglob("*.py"):
        if "_vendor" in path.parts:
            continue
        rel = path.relative_to(SRC).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
        pending: list[tuple[ast.AST, bool]] = [(tree, False)]
        while pending:
            node, inside = pending.pop()
            targets = []
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target.id]
            if "REKORDBOX_PROCESSES" in targets:
                definers.append(rel)
            if inside and isinstance(node, ast.Constant):
                enclosed.append((rel, node.lineno, node.value))
            inside = inside or isinstance(node, containers)
            pending.extend((child, inside) for child in ast.iter_child_nodes(node))
    return definers, enclosed


def test_the_process_name_list_is_defined_exactly_once_in_the_tree():
    """Only ``core.processes`` may assign the list, found by parsing every module."""
    definers = _scanned()[0]
    assert definers == ["core/processes.py"], f"the name list is assigned in {definers}"


def test_no_module_hardcodes_a_rekordbox_process_name_outside_the_one_list():
    """The process names as literals in comparisons and collections are the list's
    job. ``core.rb_writer``'s probe table is keyed by them, pinned below."""
    exempt = {"core/processes.py", "core/rb_writer.py"}
    offenders = [
        f"{rel}:{line}"
        for rel, line, value in _scanned()[1]
        if rel not in exempt and value in processes.REKORDBOX_PROCESSES
    ]
    assert not offenders, f"import REKORDBOX_PROCESSES instead of the literals at {offenders}"


def test_the_writer_has_a_probe_for_every_name_in_the_shared_list():
    """Derived from the list, so a name added without a probe fails here."""
    missing = [n for n in processes.REKORDBOX_PROCESSES if n not in rb_writer._PROCESS_PROBES]
    assert not missing, f"core.rb_writer has no probe for {missing}"


def test_an_unprobed_process_name_refuses_rather_than_being_skipped(monkeypatch):
    """A process the guard cannot ask about is one it cannot declare clear."""
    monkeypatch.setattr(
        processes, "REKORDBOX_PROCESSES", processes.REKORDBOX_PROCESSES + ("rekordboxFuture",)
    )
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    with pytest.raises(Exception) as excinfo:
        rb_writer.rekordbox_processes_running()
    assert "rekordboxFuture" in str(excinfo.value)


# Every shape a platform hands back for one process; Windows' was the unmatched one.
_PLATFORM_FORMS = {"posix": lambda name: name, "windows": lambda name: f"{name}.exe"}


@pytest.mark.parametrize("platform", sorted(_PLATFORM_FORMS))
@pytest.mark.parametrize("name", processes.REKORDBOX_PROCESSES)
def test_every_process_is_detected_in_every_platform_form(platform, name):
    """Derived from the list crossed with the platform forms, not enumerated."""
    reported = _PLATFORM_FORMS[platform](name)
    assert processes.rekordbox_processes_running(lister=lambda: (reported,)) == (name,)


def test_matching_is_exact_after_the_suffix_strip_and_never_a_substring():
    """A guard that refuses correct situations is one people bypass."""
    decoys = (
        "rekordbox-helper", "my-rekordbox-backup", "rekordboxAgentHelper", "notrekordbox",
        "rekordbox.exe.bak",
    )
    assert processes.rekordbox_processes_running(lister=lambda: decoys) == ()


def test_the_two_mechanisms_agree_on_the_same_machine_state(monkeypatch):
    """The writer (pyrekordbox, faked at its seam) and the backup module (the
    platform) agree on every combination of processes in both platform forms."""
    names = processes.REKORDBOX_PROCESSES
    for bits in range(2 ** len(names)):
        up = tuple(n for i, n in enumerate(names) if bits >> i & 1)
        for platform, form in sorted(_PLATFORM_FORMS.items()):
            reported = tuple(form(n) for n in up)
            from_backup = backup.rekordbox_processes_running(lister=lambda r=reported: r)
            monkeypatch.setattr(rb_writer, "rekordbox_running", lambda u=up: "rekordbox" in u)
            monkeypatch.setattr(
                rb_writer, "rekordbox_agent_running", lambda u=up: "rekordboxAgent" in u
            )
            from_writer = rb_writer.rekordbox_processes_running()
            assert from_backup == up, f"backup disagreed on {platform} with {up}"
            assert from_writer == ", ".join(up), f"writer disagreed on {platform} with {up}"


def test_the_empty_machine_is_clear_on_both_sides(monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    assert backup.rekordbox_processes_running(lister=tuple) == ()
    assert rb_writer.rekordbox_processes_running() == ""


def test_the_backup_module_still_exports_the_names_it_always_did():
    """The reconciliation moved the implementation, not the public surface."""
    for symbol in ("REKORDBOX_PROCESSES", "rekordbox_processes_running", "running_process_names"):
        assert symbol in backup.__all__
        assert getattr(backup, symbol) is getattr(processes, symbol)
