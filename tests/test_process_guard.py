"""The rekordbox process guard has one name list and one matching rule.

This suite exists because of a defect the U7 merge exposed. Two modules each
answered "is rekordbox running", for good reasons that still hold, and their
answers had drifted: the database writer stripped the executable suffix (via
pyrekordbox) and the backup module did not. On Windows, where psutil reports
``rekordbox.exe``, the backup guard therefore saw nothing running and would have
snapshotted a database the application was actively writing, while the database
guard on the same machine was correct. Neither module's own tests could see it.
A divergence between two guards is invisible until something puts them side by
side, so this file is that something.

Every test here DERIVES its set by walking or introspecting (seam decision P3).
Nothing is hand-listed, because a hand-listed test is one that misses the next
module to ask the same question.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.core import processes, rb_writer
from cratekit.modules.tools import backup

SRC = Path(__file__).resolve().parent.parent / "src" / "cratekit"


# ---------------------------------------------------------------------------
# One list
# ---------------------------------------------------------------------------


def _module_paths() -> list[Path]:
    return [p for p in SRC.rglob("*.py") if "_vendor" not in p.parts]


def test_the_process_name_list_is_defined_exactly_once_in_the_tree():
    """Walk the source. Only ``core.processes`` may assign the list.

    Derived by parsing every module rather than by checking the two we know
    about, so a third module that grows its own copy fails here on the day it
    lands rather than on the day the copies disagree.
    """
    definers = []
    for path in _module_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target.id]
            if "REKORDBOX_PROCESSES" in targets:
                definers.append(path.relative_to(SRC).as_posix())

    assert definers == ["core/processes.py"], (
        "the rekordbox process name list must have exactly one definition; "
        f"found assignments in {definers}"
    )


def test_no_module_hardcodes_a_rekordbox_process_name_outside_the_one_list():
    """The literals ``"rekordbox"`` and ``"rekordboxAgent"`` are the list's job.

    Scoped to comparisons and collection literals so it does not fire on prose,
    on config keys, or on the many legitimate uses of the word (seam decision
    P7: a guard that fires on correct code gets routed around). ``core.processes``
    is exempt because defining them is precisely its purpose, and
    ``core.rb_writer`` is exempt only for its probe table, which is keyed by
    those names by construction and is pinned by the coverage test below.
    """
    exempt = {"core/processes.py", "core/rb_writer.py"}
    offenders: list[str] = []
    for path in _module_paths():
        rel = path.relative_to(SRC).as_posix()
        if rel in exempt:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Tuple, ast.List, ast.Set, ast.Compare)):
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Constant) and sub.value in processes.REKORDBOX_PROCESSES:
                        offenders.append(f"{rel}:{sub.lineno}")
    assert not offenders, (
        "a rekordbox process name is hardcoded outside core.processes at "
        f"{offenders}; import REKORDBOX_PROCESSES instead"
    )


def test_the_writer_has_a_probe_for_every_name_in_the_shared_list():
    """Derived from the list, so adding a name without a probe fails here.

    The runtime behaviour is a refusal rather than a skip, which this asserts
    separately below. This test is the earlier warning.
    """
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


# ---------------------------------------------------------------------------
# One rule
# ---------------------------------------------------------------------------

# Every shape a platform can hand back for the same process. The Windows form is
# the one that was silently unmatched.
_PLATFORM_FORMS = {
    "posix": lambda name: name,
    "windows": lambda name: f"{name}.exe",
}


@pytest.mark.parametrize("platform", sorted(_PLATFORM_FORMS))
@pytest.mark.parametrize("name", processes.REKORDBOX_PROCESSES)
def test_every_process_is_detected_in_every_platform_form(platform, name):
    """Derived from the list crossed with the platform forms, not enumerated."""
    reported = _PLATFORM_FORMS[platform](name)
    assert processes.rekordbox_processes_running(lister=lambda: (reported,)) == (name,)


def test_matching_is_exact_after_the_suffix_strip_and_never_a_substring():
    """P7. A guard that refuses correct situations is one people bypass."""
    decoys = (
        "rekordbox-helper",
        "my-rekordbox-backup",
        "rekordboxAgentHelper",
        "notrekordbox",
        "rekordbox.exe.bak",
    )
    assert processes.rekordbox_processes_running(lister=lambda: decoys) == ()


def test_the_two_mechanisms_agree_on_the_same_machine_state(monkeypatch):
    """The actual regression: the writer and the backup module must not diverge.

    Drives both guards from one synthetic process table, in every combination of
    which processes are up, in both platform forms. The mechanisms stay separate
    on purpose; the ANSWERS may never differ.
    """
    names = processes.REKORDBOX_PROCESSES
    for bits in range(2 ** len(names)):
        up = tuple(n for i, n in enumerate(names) if bits >> i & 1)
        for platform, form in sorted(_PLATFORM_FORMS.items()):
            reported = tuple(form(n) for n in up)

            # The backup module's mechanism: ask the platform directly.
            from_backup = backup.rekordbox_processes_running(lister=lambda r=reported: r)

            # The writer's mechanism: ask pyrekordbox, faked at the seam the
            # writer's own tests use.
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
